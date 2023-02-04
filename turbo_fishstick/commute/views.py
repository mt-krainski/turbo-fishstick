from django.http import JsonResponse
from django.shortcuts import render
import requests

from .settings import OC_TRANSPO, TRIP_VARIANTS_BY_NAME


def index(request):
    context = get_route_summary(request.GET["trip_variant"])
    return render(request, "commute/index.html", context)


def get_route_summary(trip_variant):
    trip_details = TRIP_VARIANTS_BY_NAME[trip_variant]
    url = "https://api.octranspo1.com/v2.0/GetNextTripsForStopAllRoutes"

    # ?appID={appID}&apiKey={apiKey}&stopNo={stopNo}&format={format}"
    oc_transpo_data = requests.get(
        url,
        params={
            "appID": OC_TRANSPO["app_id"],
            "apiKey": OC_TRANSPO["api_key"],
            "stopNo": trip_details["stop_id"],
            "format": OC_TRANSPO["format"],
        },
    )

    stop_trips = oc_transpo_data.json()["GetRouteSummaryForStopResult"]

    routes = {}
    stop_metadata = {}

    stop_metadata["stop_id"] = stop_trips["StopNo"]
    stop_metadata["stop_name"] = stop_trips["StopDescription"]
    routes = [
        {
            "route_number": route["RouteNo"],
            "heading": route["RouteHeading"],
            "trips": [
                {
                    "start": trip["TripStartTime"],
                    "departure_in": trip["AdjustedScheduleTime"],
                    "last_adjusted": trip["AdjustmentAge"],
                    "adjusted": trip["AdjustmentAge"] != "-1",
                }
                for trip in route["Trips"]
            ],
        }
        for route in stop_trips["Routes"]["Route"]
    ]

    context = {"stop_metadata": stop_metadata, "routes": routes}

    return context
