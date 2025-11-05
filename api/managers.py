from django.db import models
from django.utils import timezone
from datetime import timedelta


class RecentRidesManager(models.Manager):
    def get_queryset(self):
        cutoff_time = timezone.now() - timedelta(hours=24)
        return (
            super().get_queryset().filter(pickup_time__gte=cutoff_time)
        )