from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update a staff admin user for the local operator."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--email", default="")

    def handle(self, *args, **options):
        username = options["username"].strip()
        password = options["password"]
        email = options["email"].strip()

        if not username:
            raise CommandError("Username cannot be blank.")
        if len(password) < 8:
            raise CommandError("Password must be at least 8 characters.")

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} admin user '{username}'."))
