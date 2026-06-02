from django.contrib import admin

from .models import (
    Award,
    Car,
    CarClass,
    Category,
    Division,
    Judge,
    JudgeAssignment,
    PublicVote,
    Score,
    Show,
)


class DivisionInline(admin.TabularInline):
    model = Division
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "location", "status", "public_standings")
    list_filter = ("status", "public_standings", "date")
    search_fields = ("name", "location")
    inlines = [DivisionInline, CategoryInline]


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ("name", "show", "sort_order")
    list_filter = ("show",)
    search_fields = ("name",)
    ordering = ("show", "sort_order", "name")


@admin.register(CarClass)
class CarClassAdmin(admin.ModelAdmin):
    list_display = ("name", "division", "show", "sort_order")
    list_filter = ("show", "division")
    search_fields = ("name", "division__name")
    ordering = ("show", "division__sort_order", "sort_order", "name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "show", "max_score", "sort_order")
    list_filter = ("show",)
    search_fields = ("name",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "entry_number",
        "owner_name",
        "display_vehicle",
        "car_class",
        "show",
    )
    list_filter = ("show", "car_class__division", "car_class")
    search_fields = ("entry_number", "owner_name", "make", "model", "trim")
    ordering = ("show", "entry_number")


class JudgeAssignmentInline(admin.TabularInline):
    model = JudgeAssignment
    extra = 1


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = ("name", "show", "active", "last_seen_at")
    list_filter = ("show", "active")
    search_fields = ("name",)
    readonly_fields = ("token", "last_seen_at")
    inlines = [JudgeAssignmentInline]


@admin.register(JudgeAssignment)
class JudgeAssignmentAdmin(admin.ModelAdmin):
    list_display = ("judge", "division", "car_class", "category")
    list_filter = ("judge__show", "division", "car_class", "category")
    search_fields = ("judge__name",)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        "car",
        "category",
        "judge",
        "value",
        "status",
        "submitted_at",
    )
    list_filter = ("show", "status", "category", "judge")
    search_fields = ("car__entry_number", "car__owner_name", "judge__name")
    readonly_fields = ("created_at", "updated_at", "submitted_at")


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ("show", "car_class", "place", "car")
    list_filter = ("show", "car_class")
    search_fields = ("car__entry_number", "car__owner_name")


@admin.register(PublicVote)
class PublicVoteAdmin(admin.ModelAdmin):
    list_display = ("show", "car", "voter_token", "created_at")
    list_filter = ("show",)
    search_fields = ("car__entry_number", "voter_token")
    readonly_fields = ("created_at",)
