from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Car, CarClass, Category, Division, Judge, Score, Show


class JudgingFlowTests(TestCase):
    def setUp(self):
        cache.clear()
        self.show = Show.objects.create(
            name="Demo Roundup",
            location="Local Test Lot",
            status=Show.Status.OPEN,
            public_standings=True,
        )
        self.division = Division.objects.create(show=self.show, name="1964-1973")
        self.car_class = CarClass.objects.create(
            show=self.show,
            division=self.division,
            name="Fastback",
        )
        self.category = Category.objects.create(
            show=self.show,
            name="Exterior",
            max_score=10,
        )
        self.car = Car.objects.create(
            show=self.show,
            entry_number=101,
            owner_name="Dana Driver",
            vehicle_year=1967,
            make="Ford",
            model="Mustang",
            trim="GT",
            car_class=self.car_class,
        )
        self.judge = Judge.objects.create(
            show=self.show,
            name="Judge One",
            pin="1234",
        )

    def test_judge_can_login_save_draft_and_submit_score(self):
        login_response = self.client.post(reverse("judge_login"), {"pin": "1234"})

        self.assertRedirects(login_response, reverse("judge_dashboard"))

        dashboard_response = self.client.get(reverse("judge_dashboard"))
        self.assertContains(dashboard_response, "Dana Driver")

        draft_response = self.client.post(
            reverse("score_car", args=[self.car.id]),
            {f"score_{self.category.id}": "8", "action": "draft"},
        )
        self.assertRedirects(draft_response, reverse("judge_dashboard"))
        score = Score.objects.get(judge=self.judge, car=self.car, category=self.category)
        self.assertEqual(score.value, 8)
        self.assertEqual(score.status, Score.Status.DRAFT)

        submit_response = self.client.post(
            reverse("score_car", args=[self.car.id]),
            {f"score_{self.category.id}": "9", "action": "submit"},
        )
        self.assertRedirects(submit_response, reverse("judge_dashboard"))
        score.refresh_from_db()
        self.assertEqual(score.value, 9)
        self.assertEqual(score.status, Score.Status.SUBMITTED)
        self.assertIsNotNone(score.submitted_at)

    def test_repeated_invalid_judge_pin_attempts_are_throttled(self):
        login_url = reverse("judge_login")
        for _attempt in range(5):
            response = self.client.post(login_url, {"pin": "0000"}, follow=True)
            self.assertContains(response, "That judge PIN was not accepted.")

        throttled_response = self.client.post(login_url, {"pin": "1234"}, follow=True)

        self.assertContains(throttled_response, "Too many judge PIN attempts.")
        self.assertNotIn("judge_id", self.client.session)

    def test_judge_logout_requires_post(self):
        self.client.post(reverse("judge_login"), {"pin": "1234"})

        get_response = self.client.get(reverse("judge_logout"))
        self.assertEqual(get_response.status_code, 405)
        self.assertIn("judge_id", self.client.session)

        post_response = self.client.post(reverse("judge_logout"))

        self.assertRedirects(post_response, reverse("judge_login"))
        self.assertNotIn("judge_id", self.client.session)

    def test_results_csv_requires_operator_and_exports_scores(self):
        Score.objects.create(
            show=self.show,
            judge=self.judge,
            car=self.car,
            category=self.category,
            value=9,
            status=Score.Status.SUBMITTED,
        )
        operator = User.objects.create_user(
            username="operator",
            password="password",
            is_staff=True,
        )
        self.client.force_login(operator)

        response = self.client.get(reverse("export_results_csv"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])
        self.assertContains(response, "Dana Driver")
        self.assertContains(response, "9")

    def test_ensure_admin_command_creates_staff_admin(self):
        call_command(
            "ensure_admin",
            username="showadmin",
            password="StrongPass123",
        )

        user = User.objects.get(username="showadmin")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("StrongPass123"))
