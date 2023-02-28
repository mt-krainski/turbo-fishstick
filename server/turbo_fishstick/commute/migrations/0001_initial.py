# Generated by Django 4.1.6 on 2023-02-27 01:38

from typing import Any
from django.db import migrations, models


TRIP_VARIANTS = [
    {"name": "home", "stop_name": "Rideau / Wurtemburg", "stop_id": 1845},
    {"name": "wenshan", "stop_name": "Woodroffe / Medhurst", "stop_id": 2937},
    {"name": "work", "stop_name": "Bayview", "stop_id": 3060},
]


class Migration(migrations.Migration):
    initial = True

    dependencies: Any = []

    def insertData(apps, schema_editor):
        TripVariant = apps.get_model("commute", "TripVariant")
        trips = [TripVariant(**trip_variant) for trip_variant in TRIP_VARIANTS]
        for trip in trips:
            trip.save()

    operations = [
        migrations.CreateModel(
            name="TripVariant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("stop_name", models.CharField(max_length=200)),
                ("stop_id", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RunPython(insertData),
    ]