import os

from typing import TypedDict


class OcTranspoConfig(TypedDict):
    app_id: str
    api_key: str
    format: str


OC_TRANSPO: OcTranspoConfig = {
    "app_id": os.environ["OC_TRANSPO_APP_ID"],
    "api_key": os.environ["OC_TRANSPO_APP_KEY"],
    "format": "json",
}

TRIP_VARIANTS = [
    {"name": "home", "stop_name": "Rideau / Wurtemburg", "stop_id": 1845},
    {"name": "wenshan", "stop_name": "Woodroffe / Medhurst", "stop_id": 2937},
    {"name": "work", "stop_name": "Bayview", "stop_id": 3060},
]

TRIP_VARIANTS_BY_NAME = {x["name"]: x for x in TRIP_VARIANTS}
