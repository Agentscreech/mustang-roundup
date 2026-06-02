import base64
import csv
import io
import shutil
import socket
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .models import Car, Category, Judge, Score, Show


def active_show():
    return Show.objects.order_by("-date", "-id").first()


def operator_required(view_func):
    return user_passes_test(lambda user: user.is_staff, login_url="admin:login")(
        view_func
    )


def session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key or ""


def current_judge(request):
    judge_id = request.session.get("judge_id")
    judge_token = request.session.get("judge_token")
    if not judge_id or not judge_token:
        return None
    try:
        return Judge.objects.select_related("show").get(
            id=judge_id,
            token=judge_token,
            active=True,
        )
    except Judge.DoesNotExist:
        request.session.flush()
        return None


def assigned_scope(judge):
    cars = Car.objects.filter(show=judge.show).select_related(
        "car_class",
        "car_class__division",
    )
    categories = Category.objects.filter(show=judge.show)
    assignments = list(
        judge.assignments.select_related("division", "car_class", "category")
    )

    if not assignments:
        return cars, categories

    car_filter = Q()
    assigned_category_ids = set()
    includes_all_categories = False

    for assignment in assignments:
        if assignment.car_class_id:
            car_filter |= Q(car_class=assignment.car_class)
        elif assignment.division_id:
            car_filter |= Q(car_class__division=assignment.division)
        else:
            car_filter |= Q(show=judge.show)

        if assignment.category_id:
            assigned_category_ids.add(assignment.category_id)
        else:
            includes_all_categories = True

    cars = cars.filter(car_filter).distinct()
    if not includes_all_categories:
        categories = categories.filter(id__in=assigned_category_ids)

    return cars, categories.distinct()


def expected_score_keys(show):
    keys = set()
    for judge in show.judges.filter(active=True).prefetch_related("assignments"):
        cars, categories = assigned_scope(judge)
        for car_id in cars.values_list("id", flat=True):
            for category_id in categories.values_list("id", flat=True):
                keys.add((judge.id, car_id, category_id))
    return keys


@operator_required
def dashboard(request):
    show = active_show()
    if request.method == "POST" and show:
        action = request.POST.get("action")
        if action in {"setup", "open", "closed", "finalized"}:
            show.status = action
            show.save(update_fields=["status", "updated_at"])
            messages.success(request, f"Show status changed to {show.get_status_display()}.")
        elif action == "toggle_public":
            show.public_standings = not show.public_standings
            show.save(update_fields=["public_standings", "updated_at"])
            messages.success(request, "Public standings visibility updated.")
        return redirect("dashboard")

    if not show:
        return render(request, "mustangroundup/no_show.html")

    expected = expected_score_keys(show)
    submitted_keys = set(
        show.scores.filter(status=Score.Status.SUBMITTED, value__isnull=False)
        .values_list("judge_id", "car_id", "category_id")
    )
    missing_count = len(expected - submitted_keys)
    submitted_count = len(expected & submitted_keys)
    draft_count = show.scores.filter(
        status=Score.Status.DRAFT,
        value__isnull=False,
    ).count()

    context = {
        "show": show,
        "car_count": show.cars.count(),
        "judge_count": show.judges.filter(active=True).count(),
        "category_count": show.categories.count(),
        "submitted_count": submitted_count,
        "draft_count": draft_count,
        "missing_count": missing_count,
        "expected_count": len(expected),
        "recent_judges": show.judges.filter(active=True).order_by("-last_seen_at")[:8],
    }
    return render(request, "mustangroundup/dashboard.html", context)


def judge_login(request):
    show = active_show()
    if request.method == "POST":
        if not show:
            messages.error(request, "No show has been created yet.")
            return redirect("judge_login")
        if show.status != Show.Status.OPEN:
            messages.error(request, "Judging is not open yet.")
            return redirect("judge_login")

        pin = request.POST.get("pin", "").strip()
        try:
            judge = show.judges.get(pin=pin, active=True)
        except Judge.DoesNotExist:
            messages.error(request, "That judge PIN was not found.")
            return redirect("judge_login")

        request.session["judge_id"] = judge.id
        request.session["judge_token"] = judge.token
        judge.mark_seen()
        return redirect("judge_dashboard")

    return render(request, "mustangroundup/judge_login.html", {"show": show})


def judge_logout(request):
    request.session.pop("judge_id", None)
    request.session.pop("judge_token", None)
    messages.success(request, "You have been signed out.")
    return redirect("judge_login")


def judge_dashboard(request):
    judge = current_judge(request)
    if not judge:
        return redirect("judge_login")

    judge.mark_seen()
    cars, categories = assigned_scope(judge)
    category_list = list(categories)
    score_rows = []
    score_map = {
        (score.car_id, score.category_id): score
        for score in Score.objects.filter(judge=judge, car__in=cars, category__in=category_list)
    }

    for car in cars:
        car_scores = [score_map.get((car.id, category.id)) for category in category_list]
        submitted = [
            score
            for score in car_scores
            if score and score.status == Score.Status.SUBMITTED and score.value is not None
        ]
        drafts = [score for score in car_scores if score and score.value is not None]
        if len(submitted) == len(category_list) and category_list:
            status = "Submitted"
        elif drafts:
            status = "Draft saved"
        else:
            status = "Not started"
        score_rows.append({"car": car, "status": status})

    return render(
        request,
        "mustangroundup/judge_dashboard.html",
        {
            "judge": judge,
            "show": judge.show,
            "cars": score_rows,
            "categories": category_list,
        },
    )


def score_car(request, car_id):
    judge = current_judge(request)
    if not judge:
        return redirect("judge_login")
    if judge.show.status != Show.Status.OPEN:
        messages.error(request, "Judging is closed.")
        return redirect("judge_dashboard")

    cars, categories = assigned_scope(judge)
    car = get_object_or_404(cars, id=car_id)
    category_list = list(categories)
    existing_scores = {
        score.category_id: score
        for score in Score.objects.filter(judge=judge, car=car, category__in=category_list)
    }

    if request.method == "POST":
        action = request.POST.get("action", "draft")
        status = Score.Status.SUBMITTED if action == "submit" else Score.Status.DRAFT
        parsed_values = {}
        errors = []

        for category in category_list:
            raw_value = request.POST.get(f"score_{category.id}", "").strip()
            if raw_value == "":
                parsed_values[category.id] = None
                if status == Score.Status.SUBMITTED:
                    errors.append(f"{category.name} is required before final submit.")
                continue
            try:
                value = int(raw_value)
            except ValueError:
                errors.append(f"{category.name} must be a whole number.")
                continue
            if value < 0 or value > category.max_score:
                errors.append(f"{category.name} must be between 0 and {category.max_score}.")
                continue
            parsed_values[category.id] = value

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            for category in category_list:
                score, _created = Score.objects.get_or_create(
                    show=judge.show,
                    judge=judge,
                    car=car,
                    category=category,
                    defaults={"device_session": session_key(request)},
                )
                score.value = parsed_values[category.id]
                score.status = status
                score.device_session = session_key(request)
                score.full_clean()
                score.save()
            messages.success(
                request,
                "Final scores submitted." if status == Score.Status.SUBMITTED else "Draft saved.",
            )
            return redirect("judge_dashboard")

    score_rows = [
        {"category": category, "score": existing_scores.get(category.id)}
        for category in category_list
    ]
    return render(
        request,
        "mustangroundup/score_car.html",
        {
            "judge": judge,
            "show": judge.show,
            "car": car,
            "score_rows": score_rows,
        },
    )


def build_results(show):
    results = []
    submitted_scores = Score.objects.filter(
        show=show,
        status=Score.Status.SUBMITTED,
        value__isnull=False,
    ).select_related("car", "category")

    score_totals = {}
    score_counts = {}
    for score in submitted_scores:
        score_totals[score.car_id] = score_totals.get(score.car_id, 0) + score.value
        score_counts[score.car_id] = score_counts.get(score.car_id, 0) + 1

    for car_class in show.classes.select_related("division").prefetch_related("cars"):
        rows = []
        for car in car_class.cars.all():
            rows.append(
                {
                    "car": car,
                    "total": score_totals.get(car.id, 0),
                    "score_count": score_counts.get(car.id, 0),
                }
            )
        rows.sort(key=lambda item: (-item["total"], item["car"].entry_number))
        results.append({"car_class": car_class, "rows": rows})
    return results


def results(request):
    show = active_show()
    if not show:
        raise Http404("No show configured.")
    if not show.public_standings and not request.user.is_staff:
        messages.error(request, "Results are not public yet.")
        return redirect("judge_login")
    return render(
        request,
        "mustangroundup/results.html",
        {"show": show, "results": build_results(show)},
    )


@operator_required
def export_results_csv(request):
    show = active_show()
    if not show:
        raise Http404("No show configured.")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{show.date}-results.csv"'
    writer = csv.writer(response)
    writer.writerow(["Class", "Place", "Entry", "Owner", "Vehicle", "Total", "Scores"])
    for class_result in build_results(show):
        for place, row in enumerate(class_result["rows"], start=1):
            car = row["car"]
            writer.writerow(
                [
                    class_result["car_class"].name,
                    place,
                    car.entry_number,
                    car.owner_name,
                    car.display_vehicle,
                    row["total"],
                    row["score_count"],
                ]
            )
    return response


def local_ip_addresses():
    addresses = {"127.0.0.1"}
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            addresses.add(info[4][0])
    except socket.gaierror:
        pass
    return sorted(addresses)


def qr_data_url(value):
    try:
        import qrcode
    except ImportError:
        return ""
    image = qrcode.make(value)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


@operator_required
def diagnostics(request):
    show = active_show()
    login_url = request.build_absolute_uri(reverse("judge_login"))

    if request.method == "POST" and request.POST.get("action") == "backup":
        database_name = settings.DATABASES["default"]["NAME"]
        database_path = Path(database_name)
        if database_path.exists():
            backup_dir = Path(settings.BASE_DIR) / "backups"
            backup_dir.mkdir(exist_ok=True)
            backup_path = backup_dir / f"mustang-roundup-{timezone.now():%Y%m%d-%H%M%S}.sqlite3"
            shutil.copy2(database_path, backup_path)
            messages.success(request, f"Database backup created: {backup_path.name}")
        else:
            messages.error(request, "SQLite database file was not found.")
        return redirect("diagnostics")

    return render(
        request,
        "mustangroundup/diagnostics.html",
        {
            "show": show,
            "login_url": login_url,
            "ip_addresses": local_ip_addresses(),
            "qr_code": qr_data_url(login_url),
            "database_path": settings.DATABASES["default"]["NAME"],
        },
    )


def manifest(request):
    return JsonResponse(
        {
            "name": "Mustang Roundup Judging",
            "short_name": "Roundup",
            "start_url": reverse("judge_login"),
            "display": "standalone",
            "background_color": "#f8fafc",
            "theme_color": "#13315c",
            "icons": [],
        }
    )


def service_worker(request):
    static_css = settings.STATIC_URL + "css/roundup.css"
    body = f"""
const CACHE_NAME = "mustang-roundup-shell-v1";
const SHELL = ["{reverse('judge_login')}", "{static_css}"];

self.addEventListener("install", event => {{
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(SHELL)));
}});

self.addEventListener("activate", event => {{
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)))
    )
  );
}});

self.addEventListener("fetch", event => {{
  if (event.request.method !== "GET") return;
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request).then(response => response || caches.match("{reverse('judge_login')}")))
  );
}});
"""
    return HttpResponse(body, content_type="text/javascript")




