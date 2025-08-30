from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import OTP, UserProfile
from .serializers import (
    UserRegistrationSerializer, 
    OTPVerificationSerializer, 
    UserLoginSerializer,
    UserDetailSerializer
)

@extend_schema(
    summary="User Registration",
    description="Register a new user and send OTP to email for verification",
    request=UserRegistrationSerializer,
    responses={201: {"description": "Registration successful, OTP sent to email"}}
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user and send OTP for email verification"""
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Create user but don't activate yet
        user = User.objects.create_user(
            username=email,  # Use email as username
            email=email,
            password=password,
            is_active=False  # User inactive until email verification
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        # Generate and send OTP
        otp = OTP.objects.create(email=email)
        
        # Send OTP email
        try:
            send_mail(
                subject='Email Verification OTP',
                message=f'Your OTP for email verification is: {otp.otp_code}\n\nThis OTP will expire in 10 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            print(f"OTP sent to {email}: {otp.otp_code}")  # For development
        except Exception as e:
            print(f"Email sending failed: {e}")
            # In development, we'll continue anyway
            pass
        
        return Response({
            'message': 'Registration successful. OTP sent to your email for verification.',
            'email': email,
            'otp_code': otp.otp_code  # Remove in production
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Verify Registration OTP",
    description="Verify the OTP sent during registration to activate the account",
    request=OTPVerificationSerializer,
    responses={200: {"description": "Email verified successfully"}}
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_registration(request):
    """Verify the OTP sent during registration"""
    serializer = OTPVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        
        try:
            # Find valid OTP
            otp = OTP.objects.filter(
                email=email,
                otp_code=otp_code,
                is_verified=False
            ).latest('created_at')
            
            if otp.is_expired():
                return Response({
                    'error': 'OTP has expired. Please register again.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verify OTP
            otp.is_verified = True
            otp.save()
            
            # Activate user account
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            
            # Mark profile as email verified
            profile = user.profile
            profile.email_verified = True
            profile.save()
            
            return Response({
                'message': 'Email verified successfully. You can now login.',
                'email': email
            }, status=status.HTTP_200_OK)
            
        except OTP.DoesNotExist:
            return Response({
                'error': 'Invalid OTP or OTP not found.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found.'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="User Login",
    description="Login user with email and password, set auth_token cookie",
    request=UserLoginSerializer,
    responses={200: {"description": "Login successful, auth_token cookie set"}}
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login user and set auth_token in HTTP-only cookie"""
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response({
                    'error': 'Account not verified. Please verify your email first.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Authenticate using username (which is email)
            authenticated_user = authenticate(request, username=email, password=password)
            
            if authenticated_user:
                login(request, authenticated_user)
                
                response = Response({
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'email_verified': user.profile.email_verified
                    }
                }, status=status.HTTP_200_OK)
                
                # Set auth_token cookie (using sessionid as the token)
                response.set_cookie(
                    'auth_token',
                    request.session.session_key,
                    max_age=3600,  # 1 hour
                    httponly=True,
                    secure=False,  # Set to True in production with HTTPS
                    samesite='Lax'
                )
                
                return response
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Get User Details",
    description="Get details of the currently logged-in user",
    responses={200: UserDetailSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    """Get details of the logged-in user"""
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary="User Logout",
    description="Logout user and clear auth_token cookie",
    responses={200: {"description": "Logout successful"}}
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Logout user and clear auth_token cookie"""
    logout(request)
    
    response = Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)
    
    # Clear auth_token cookie
    response.delete_cookie('auth_token')
    
    return response
