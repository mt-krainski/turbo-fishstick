from django.db import models


class TripVariant(models.Model):
    name = models.CharField(max_length=200, unique=True)
    stop_name = models.CharField(max_length=200)
    stop_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.stop_name})"
