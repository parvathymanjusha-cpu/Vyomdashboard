
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Telemetry


# =========================
# DASHBOARD PAGES
# =========================

def dashboard(request):
    return render(request, "telemetry/dashboard.html")


def live_telemetry(request):
    return render(request, "telemetry/live_telemetry.html")


def graphs(request):
    return render(request, "telemetry/graphs.html")


def location(request):
    return render(request, "telemetry/location.html")


def telemetry_log(request):
    return render(request, "telemetry/telemetry_log.html")


def mission_info(request):
    return render(request, "telemetry/mission_info.html")


def settings_page(request):
    return render(request, "telemetry/settings.html")


# =========================
# TELEMETRY API
# =========================

@csrf_exempt
def receive_telemetry(request):

    # -------------------------
    # GET: READ LATEST TELEMETRY
    # -------------------------

    if request.method == "GET":

        telemetry = Telemetry.objects.order_by("-timestamp").first()

        if telemetry is None:
            return JsonResponse({
                "success": False,
                "message": "No telemetry data available."
            }, status=404)

        return JsonResponse({
            "success": True,
            "temperature": telemetry.temperature,
            "humidity": telemetry.humidity,
            "latitude": telemetry.latitude,
            "longitude": telemetry.longitude,
            "timestamp": telemetry.timestamp.isoformat()
        })


    # -------------------------
    # POST: RECEIVE TELEMETRY
    # -------------------------

    if request.method != "POST":

        return JsonResponse({
            "success": False,
            "message": "Only GET and POST requests are allowed."
        }, status=405)


    try:

        data = json.loads(request.body)

        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])


    except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError
    ):

        return JsonResponse({
            "success": False,
            "message": "Invalid telemetry data."
        }, status=400)


    # -------------------------
    # SAVE TELEMETRY TO DATABASE
    # -------------------------

    telemetry = Telemetry.objects.create(

        temperature=temperature,
        humidity=humidity,
        latitude=latitude,
        longitude=longitude

    )


    # -------------------------
    # RETURN SUCCESS RESPONSE
    # -------------------------

    return JsonResponse({

        "success": True,

        "message": "Telemetry received successfully.",

        "telemetry": {

            "temperature": telemetry.temperature,
            "humidity": telemetry.humidity,
            "latitude": telemetry.latitude,
            "longitude": telemetry.longitude,
            "timestamp": telemetry.timestamp.isoformat()

        }

    }, status=201)
