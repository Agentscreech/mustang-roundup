from django.core.management.base import BaseCommand

from mustangroundup.models import Car, CarClass, Category, Division, Judge, JudgeAssignment, Show


class Command(BaseCommand):
    help = "Create a small local demo show with cars, categories, and judges."

    def handle(self, *args, **options):
        show, _created = Show.objects.get_or_create(
            name="Demo Mustang Roundup",
            defaults={
                "location": "Local Wi-Fi Show Lot",
                "status": Show.Status.OPEN,
                "public_standings": True,
            },
        )
        division, _created = Division.objects.get_or_create(
            show=show,
            name="Classic",
            defaults={"sort_order": 1},
        )
        car_class, _created = CarClass.objects.get_or_create(
            show=show,
            division=division,
            name="1964-1973",
            defaults={"sort_order": 1},
        )
        categories = [
            Category.objects.get_or_create(
                show=show,
                name=name,
                defaults={"max_score": 10, "sort_order": index},
            )[0]
            for index, name in enumerate(["Exterior", "Interior", "Engine"], start=1)
        ]
        cars = [
            (101, "Alex Avery", 1965, "Coupe"),
            (102, "Blake Bennett", 1967, "Fastback GT"),
            (103, "Casey Cruz", 1970, "Mach 1"),
        ]
        for entry_number, owner, year, trim in cars:
            Car.objects.get_or_create(
                show=show,
                entry_number=entry_number,
                defaults={
                    "owner_name": owner,
                    "vehicle_year": year,
                    "make": "Ford",
                    "model": "Mustang",
                    "trim": trim,
                    "car_class": car_class,
                },
            )

        judge, _created = Judge.objects.get_or_create(
            show=show,
            pin="1234",
            defaults={"name": "Demo Judge"},
        )
        for category in categories:
            JudgeAssignment.objects.get_or_create(judge=judge, category=category)

        self.stdout.write(self.style.SUCCESS("Demo show ready. Judge PIN: 1234"))
