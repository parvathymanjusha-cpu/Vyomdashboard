from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("live/", views.live_telemetry, name="live_telemetry"),
    path("graphs/", views.graphs, name="graphs"),
    path("location/", views.location, name="location"),
    path("log/", views.telemetry_log, name="telemetry_log"),
    path("mission/", views.mission_info, name="mission_info"),
    path("settings/", views.settings_page, name="settings"),

    # Real telemetry API
    path(
        "api/telemetry/",
        views.receive_telemetry,
        name="receive_telemetry"
    ),
]