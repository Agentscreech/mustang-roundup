# Generated for the local-first Mustang Roundup rebuild.

import django.db.models.deletion
import django.utils.timezone
import mustangroundup.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Show",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("date", models.DateField(default=django.utils.timezone.localdate)),
                ("location", models.CharField(blank=True, max_length=200)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("setup", "Setup"),
                            ("open", "Open for judging"),
                            ("closed", "Judging closed"),
                            ("finalized", "Finalized"),
                        ],
                        default="setup",
                        max_length=20,
                    ),
                ),
                ("public_standings", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-date", "name"]},
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("max_score", models.PositiveIntegerField(default=10)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                (
                    "show",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="categories", to="mustangroundup.show"),
                ),
            ],
            options={"ordering": ["sort_order", "name"]},
        ),
        migrations.CreateModel(
            name="Division",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                (
                    "show",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="divisions", to="mustangroundup.show"),
                ),
            ],
            options={"ordering": ["sort_order", "name"]},
        ),
        migrations.CreateModel(
            name="Judge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("pin", models.CharField(max_length=32)),
                ("token", models.CharField(default=mustangroundup.models.make_judge_token, max_length=64, unique=True)),
                ("active", models.BooleanField(default=True)),
                ("device_lock", models.CharField(blank=True, max_length=128)),
                ("last_seen_at", models.DateTimeField(blank=True, null=True)),
                (
                    "show",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="judges", to="mustangroundup.show"),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="CarClass",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                (
                    "division",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="classes", to="mustangroundup.division"),
                ),
                (
                    "show",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="classes", to="mustangroundup.show"),
                ),
            ],
            options={
                "verbose_name": "class",
                "verbose_name_plural": "classes",
                "ordering": ["division__sort_order", "sort_order", "name"],
            },
        ),
        migrations.CreateModel(
            name="Car",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("entry_number", models.PositiveIntegerField()),
                ("owner_name", models.CharField(max_length=200)),
                ("vehicle_year", models.PositiveIntegerField(blank=True, null=True)),
                ("make", models.CharField(default="Ford", max_length=100)),
                ("model", models.CharField(default="Mustang", max_length=100)),
                ("trim", models.CharField(blank=True, max_length=100)),
                ("notes", models.TextField(blank=True)),
                (
                    "car_class",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="cars", to="mustangroundup.carclass", verbose_name="class"),
                ),
                (
                    "show",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cars", to="mustangroundup.show"),
                ),
            ],
            options={"ordering": ["entry_number"]},
        ),
        migrations.CreateModel(
            name="JudgeAssignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "car_class",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="judge_assignments", to="mustangroundup.carclass", verbose_name="class"),
                ),
                (
                    "category",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="judge_assignments", to="mustangroundup.category"),
                ),
                (
                    "division",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="judge_assignments", to="mustangroundup.division"),
                ),
                (
                    "judge",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="assignments", to="mustangroundup.judge"),
                ),
            ],
            options={"ordering": ["judge__name", "division__sort_order", "car_class__sort_order"]},
        ),
        migrations.CreateModel(
            name="Award",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("place", models.PositiveIntegerField()),
                (
                    "car",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="awards", to="mustangroundup.car"),
                ),
                (
                    "car_class",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="awards", to="mustangroundup.carclass", verbose_name="class"),
                ),
                (
                    "show",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="awards", to="mustangroundup.show"),
                ),
            ],
            options={"ordering": ["car_class__sort_order", "place"]},
        ),
        migrations.CreateModel(
            name="PublicVote",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("voter_token", models.CharField(max_length=128)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "car",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="public_votes", to="mustangroundup.car"),
                ),
                (
                    "show",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="public_votes", to="mustangroundup.show"),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Score",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.PositiveIntegerField(blank=True, null=True)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("submitted", "Submitted")], default="draft", max_length=20)),
                ("device_session", models.CharField(blank=True, max_length=128)),
                ("submitted_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "car",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="scores", to="mustangroundup.car"),
                ),
                (
                    "category",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="scores", to="mustangroundup.category"),
                ),
                (
                    "judge",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="scores", to="mustangroundup.judge"),
                ),
                (
                    "show",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="scores", to="mustangroundup.show"),
                ),
            ],
            options={"ordering": ["car__entry_number", "category__sort_order"]},
        ),
        migrations.AddConstraint(
            model_name="award",
            constraint=models.UniqueConstraint(fields=("show", "car_class", "place"), name="unique_award_place_per_class"),
        ),
        migrations.AddConstraint(
            model_name="car",
            constraint=models.UniqueConstraint(fields=("show", "entry_number"), name="unique_entry_number_per_show"),
        ),
        migrations.AddConstraint(
            model_name="carclass",
            constraint=models.UniqueConstraint(fields=("show", "division", "name"), name="unique_class_name_per_division"),
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(fields=("show", "name"), name="unique_category_name_per_show"),
        ),
        migrations.AddConstraint(
            model_name="division",
            constraint=models.UniqueConstraint(fields=("show", "name"), name="unique_division_name_per_show"),
        ),
        migrations.AddConstraint(
            model_name="judge",
            constraint=models.UniqueConstraint(fields=("show", "pin"), name="unique_judge_pin_per_show"),
        ),
        migrations.AddConstraint(
            model_name="publicvote",
            constraint=models.UniqueConstraint(fields=("show", "voter_token"), name="unique_public_vote_token_per_show"),
        ),
        migrations.AddConstraint(
            model_name="score",
            constraint=models.UniqueConstraint(fields=("judge", "car", "category"), name="unique_score_per_judge_car_category"),
        ),
    ]
