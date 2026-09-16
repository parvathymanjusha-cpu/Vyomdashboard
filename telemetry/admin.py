from django.contrib import admin
from .models import Telemetry


@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "temperature",
        "humidity",
        "latitude",
        "longitude",
    )

    ordering = ("-timestamp",)