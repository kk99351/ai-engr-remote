from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('register/verify/', views.verify_registration, name='verify_registration'),
    path('login/', views.login_user, name='login'),
    path('me/', views.get_user_details, name='user_details'),
    path('logout/', views.logout_user, name='logout'),
]
