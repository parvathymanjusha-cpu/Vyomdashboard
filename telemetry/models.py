from django.db import models


class Telemetry(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.temperature}°C"