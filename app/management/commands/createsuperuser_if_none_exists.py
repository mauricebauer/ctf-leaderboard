import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    Create a superuser if none exist
    Example:
        manage.py createsuperuser_if_none_exists
    """

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):

        User = get_user_model()
        if User.objects.exists():
            return

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

        User.objects.create_superuser(
            username=username, password=password, email=email)

        self.stdout.write(f'Local user "{username}" was created')
