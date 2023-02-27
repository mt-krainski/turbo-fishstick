from django.http import JsonResponse, Http404
from django.shortcuts import render
from rest_framework import serializers
import requests

from .models import TripVariant
from .settings import OC_TRANSPO


class TripVariantSerializer(serializers.Serializer):
    trip_variant = serializers.ChoiceField(
        [(trip.name, trip.stop_name) for trip in TripVariant.objects.all()]
    )


def index(request):
    serializer = TripVariantSerializer(request.GET)
    context = _route_summary(serializer.data["trip_variant"])
    return render(request, "commute/index.html", context)


def get_route_summary(request):
    serializer = TripVariantSerializer(request.GET)
    route_summary = _route_summary(serializer.data["trip_variant"])
    return JsonResponse(route_summary)


def _route_summary(trip_variant):
    try:
        trip_details = TripVariant.objects.get(name=trip_variant)
    except TripVariant.DoesNotExist:
        raise Http404("Trip variant does not exist")

    # Request based on
    # https://www.octranspo.com/en/plan-your-trip/travel-tools/developers/dev-doc
    url = "https://api.octranspo1.com/v2.0/GetNextTripsForStopAllRoutes"
    oc_transpo_data = requests.get(
        url,
        params={
            "appID": OC_TRANSPO["app_id"],
            "apiKey": OC_TRANSPO["api_key"],
            "stopNo": trip_details.stop_id,
            "format": OC_TRANSPO["format"],
        },
    )

    stop_trips = oc_transpo_data.json()["GetRouteSummaryForStopResult"]

    routes = {}
    stop_metadata = {}

    stop_metadata["stop_id"] = stop_trips["StopNo"]
    stop_metadata["stop_name"] = stop_trips["StopDescription"]

    if not isinstance(stop_trips["Routes"]["Route"], list):
        stop_trips["Routes"]["Route"] = [stop_trips["Routes"]["Route"]]

    routes = []

    for route in stop_trips["Routes"]["Route"]:
        if not isinstance(route["Trips"], list):
            route["Trips"] = [route["Trips"]]

        routes.append(
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
        )

    context = {"stop_metadata": stop_metadata, "routes": routes}

    return context
