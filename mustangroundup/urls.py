from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("diagnostics/", views.diagnostics, name="diagnostics"),
    path("judge/login/", views.judge_login, name="judge_login"),
    path("judge/logout/", views.judge_logout, name="judge_logout"),
    path("judge/", views.judge_dashboard, name="judge_dashboard"),
    path("judge/car/<int:car_id>/", views.score_car, name="score_car"),
    path("results/", views.results, name="results"),
    path("results.csv", views.export_results_csv, name="export_results_csv"),
    path("manifest.json", views.manifest, name="manifest"),
    path("service-worker.js", views.service_worker, name="service_worker"),
]
