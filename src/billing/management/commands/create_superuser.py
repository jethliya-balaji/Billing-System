# management command to create a superuser for production deployment
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class Command(BaseCommand):
    help = 'Creates a superuser for production deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username for the superuser (default: admin)',
            default='admin'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email for the superuser',
            default=''
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the superuser'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force create superuser even if one already exists',
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        force = options['force']

        # Try to get credentials from environment variables if not provided
        if not username:
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        
        if not email:
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        
        if not password:
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists() and not force:
            self.stdout.write(
                self.style.WARNING('A superuser already exists. Use --force to create anyway.')
            )
            return

        # Validate required fields
        if not password:
            self.stdout.write(
                self.style.ERROR(
                    'Password is required. Provide it via --password argument '
                    'or DJANGO_SUPERUSER_PASSWORD environment variable.'
                )
            )
            return

        # Validate password strength
        try:
            validate_password(password)
        except ValidationError as e:
            self.stdout.write(
                self.style.ERROR(f'Password validation failed: {"; ".join(e.messages)}')
            )
            return

        # Check if user with this username already exists
        if User.objects.filter(username=username).exists():
            if force:
                # Delete existing user if force is enabled
                existing_user = User.objects.get(username=username)
                existing_user.delete()
                self.stdout.write(
                    self.style.WARNING(f'Deleted existing user: {username}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'User with username "{username}" already exists. '
                        'Use --force to replace the existing user.'
                    )
                )
                return

        try:
            # Create the superuser
            superuser = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser: {username}'
                    f'{f" ({email})" if email else ""}'
                )
            )
            
            # Additional info for production
            self.stdout.write(
                self.style.NOTICE(
                    'IMPORTANT: Remember to:\n'
                    '1. Change the default password after first login\n'
                    '2. Remove or secure environment variables containing credentials\n'
                    '3. Set up proper user permissions for other staff members'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )
            raise