from django.core.management.base import BaseCommand
from api.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database with sample data...')

        # Create categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Electronic devices and gadgets'
            },
            {
                'name': 'Clothing',
                'description': 'Apparel and fashion items'
            },
            {
                'name': 'Books',
                'description': 'Books and educational materials'
            },
            {
                'name': 'Home & Garden',
                'description': 'Home improvement and garden supplies'
            },
            {
                'name': 'Sports',
                'description': 'Sports equipment and accessories'
            }
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'description': 'Latest iPhone with advanced camera system',
                'price': Decimal('999.99'),
                'category': categories[0],  # Electronics
                'stock_quantity': 25
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Flagship Android smartphone',
                'price': Decimal('899.99'),
                'category': categories[0],  # Electronics
                'stock_quantity': 30
            },
            {
                'name': 'MacBook Air M3',
                'description': 'Lightweight laptop with M3 chip',
                'price': Decimal('1199.99'),
                'category': categories[0],  # Electronics
                'stock_quantity': 15
            },
            {
                'name': 'Nike Air Max 90',
                'description': 'Classic running shoes',
                'price': Decimal('129.99'),
                'category': categories[1],  # Clothing
                'stock_quantity': 50
            },
            {
                'name': 'Levi\'s 501 Jeans',
                'description': 'Original fit jeans',
                'price': Decimal('89.99'),
                'category': categories[1],  # Clothing
                'stock_quantity': 40
            },
            {
                'name': 'The Python Programming Language',
                'description': 'Complete guide to Python programming',
                'price': Decimal('49.99'),
                'category': categories[2],  # Books
                'stock_quantity': 20
            },
            {
                'name': 'Django for Beginners',
                'description': 'Learn web development with Django',
                'price': Decimal('39.99'),
                'category': categories[2],  # Books
                'stock_quantity': 15
            },
            {
                'name': 'Garden Tool Set',
                'description': 'Complete set of essential garden tools',
                'price': Decimal('79.99'),
                'category': categories[3],  # Home & Garden
                'stock_quantity': 10
            },
            {
                'name': 'Basketball',
                'description': 'Official size basketball',
                'price': Decimal('29.99'),
                'category': categories[4],  # Sports
                'stock_quantity': 35
            },
            {
                'name': 'Tennis Racket',
                'description': 'Professional tennis racket',
                'price': Decimal('149.99'),
                'category': categories[4],  # Sports
                'stock_quantity': 12
            }
        ]

        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated database with {len(categories)} categories and {len(products_data)} products'
            )
        )
