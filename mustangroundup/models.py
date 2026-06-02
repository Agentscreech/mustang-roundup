import secrets

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Show(models.Model):
    class Status(models.TextChoices):
        SETUP = "setup", "Setup"
        OPEN = "open", "Open for judging"
        CLOSED = "closed", "Judging closed"
        FINALIZED = "finalized", "Finalized"

    name = models.CharField(max_length=200)
    date = models.DateField(default=timezone.localdate)
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SETUP,
    )
    public_standings = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "name"]

    def __str__(self):
        return f"{self.name} ({self.date:%Y})"


class Division(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="divisions")
    name = models.CharField(max_length=200)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["show", "name"],
                name="unique_division_name_per_show",
            )
        ]

    def __str__(self):
        return f"{self.show.name}: {self.name}"


class CarClass(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="classes")
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name="classes",
    )
    name = models.CharField(max_length=200)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "class"
        verbose_name_plural = "classes"
        ordering = ["division__sort_order", "sort_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["show", "division", "name"],
                name="unique_class_name_per_division",
            )
        ]

    def clean(self):
        if self.division_id and self.show_id and self.division.show_id != self.show_id:
            raise ValidationError("Class division must belong to the same show.")

    def __str__(self):
        return f"{self.division.name}: {self.name}"


class Category(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=200)
    max_score = models.PositiveIntegerField(default=10)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["sort_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["show", "name"],
                name="unique_category_name_per_show",
            )
        ]

    def __str__(self):
        return f"{self.show.name}: {self.name}"


class Car(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="cars")
    entry_number = models.PositiveIntegerField()
    owner_name = models.CharField(max_length=200)
    vehicle_year = models.PositiveIntegerField(null=True, blank=True)
    make = models.CharField(max_length=100, default="Ford")
    model = models.CharField(max_length=100, default="Mustang")
    trim = models.CharField(max_length=100, blank=True)
    car_class = models.ForeignKey(
        CarClass,
        on_delete=models.PROTECT,
        related_name="cars",
        verbose_name="class",
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["entry_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["show", "entry_number"],
                name="unique_entry_number_per_show",
            )
        ]

    def clean(self):
        if self.car_class_id and self.show_id and self.car_class.show_id != self.show_id:
            raise ValidationError("Car class must belong to the same show.")

    @property
    def display_vehicle(self):
        parts = [str(self.vehicle_year or ""), self.make, self.model, self.trim]
        return " ".join(part for part in parts if part).strip()

    def __str__(self):
        return f"#{self.entry_number} {self.owner_name} - {self.display_vehicle}"


def make_judge_token():
    return secrets.token_urlsafe(18)


class Judge(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="judges")
    name = models.CharField(max_length=200)
    pin = models.CharField(max_length=32)
    token = models.CharField(max_length=64, unique=True, default=make_judge_token)
    active = models.BooleanField(default=True)
    device_lock = models.CharField(max_length=128, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["show", "pin"],
                name="unique_judge_pin_per_show",
            )
        ]

    def mark_seen(self):
        self.last_seen_at = timezone.now()
        self.save(update_fields=["last_seen_at"])

    def __str__(self):
        return f"{self.name} ({self.show.name})"


class JudgeAssignment(models.Model):
    judge = models.ForeignKey(
        Judge,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name="judge_assignments",
        null=True,
        blank=True,
    )
    car_class = models.ForeignKey(
        CarClass,
        on_delete=models.CASCADE,
        related_name="judge_assignments",
        null=True,
        blank=True,
        verbose_name="class",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="judge_assignments",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["judge__name", "division__sort_order", "car_class__sort_order"]

    def clean(self):
        show_id = self.judge.show_id if self.judge_id else None
        related = [self.division, self.car_class, self.category]
        for item in related:
            if item and item.show_id != show_id:
                raise ValidationError("Assignments must stay within the judge's show.")
        if self.car_class and self.division and self.car_class.division_id != self.division_id:
            raise ValidationError("Assigned class must belong to the assigned division.")

    def __str__(self):
        scopes = [
            self.division.name if self.division else "all divisions",
            self.car_class.name if self.car_class else "all classes",
            self.category.name if self.category else "all categories",
        ]
        return f"{self.judge.name}: {', '.join(scopes)}"


class Score(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"

    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="scores")
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name="scores")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="scores")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="scores",
    )
    value = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    device_session = models.CharField(max_length=128, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["car__entry_number", "category__sort_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["judge", "car", "category"],
                name="unique_score_per_judge_car_category",
            )
        ]

    def clean(self):
        show_id = self.show_id
        for relation in [self.judge, self.car, self.category]:
            if relation and relation.show_id != show_id:
                raise ValidationError("Score relations must belong to the same show.")
        if self.value is not None and self.category_id and self.value > self.category.max_score:
            raise ValidationError(
                {"value": f"Score cannot exceed {self.category.max_score}."}
            )

    def save(self, *args, **kwargs):
        if self.status == self.Status.SUBMITTED and self.submitted_at is None:
            self.submitted_at = timezone.now()
        if self.status == self.Status.DRAFT:
            self.submitted_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.judge.name} scored #{self.car.entry_number} {self.category.name}"


class Award(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="awards")
    car_class = models.ForeignKey(
        CarClass,
        on_delete=models.CASCADE,
        related_name="awards",
        verbose_name="class",
    )
    place = models.PositiveIntegerField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="awards")

    class Meta:
        ordering = ["car_class__sort_order", "place"]
        constraints = [
            models.UniqueConstraint(
                fields=["show", "car_class", "place"],
                name="unique_award_place_per_class",
            )
        ]

    def clean(self):
        if self.car_id and self.show_id and self.car.show_id != self.show_id:
            raise ValidationError("Award car must belong to the same show.")
        if self.car_class_id and self.show_id and self.car_class.show_id != self.show_id:
            raise ValidationError("Award class must belong to the same show.")

    def __str__(self):
        return f"{self.car_class.name} place {self.place}: #{self.car.entry_number}"


class PublicVote(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="public_votes")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="public_votes")
    voter_token = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["show", "voter_token"],
                name="unique_public_vote_token_per_show",
            )
        ]

    def clean(self):
        if self.car_id and self.show_id and self.car.show_id != self.show_id:
            raise ValidationError("Public vote car must belong to the same show.")

    def __str__(self):
        return f"{self.show.name}: public vote for #{self.car.entry_number}"
