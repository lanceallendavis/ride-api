from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import RecentRidesManager


class RideUser(AbstractUser):
    class RoleChoices(models.TextChoices):
        ADMIN = 'AD', 'Admin'
        DRIVER = 'DR', 'Driver'
        RIDER = 'RD', 'Rider'
        EMPLOYEE = 'EM', 'Employee'

    role = models.CharField(
        max_length=10,
        choices=RoleChoices.choices,
        default=RoleChoices.RIDER
    )
    phone_number = models.CharField(
        max_length=15, unique=True, null=True
    )
    
    def __str__(self):
        return f'{self.username}({self.get_role_display()})'
    


class Ride(models.Model):
    class StatusChoices(models.TextChoices):
        PICKUP = 'PU', 'Pick-Up'
        CANCELLED = 'CA', 'Cancelled'
        ENROUTE = 'ER', 'En-route'
        DROPOFF = 'DO', 'Drop-off'
        COMPLETED = 'CP', 'Completed'

    rider = models.ForeignKey(
        RideUser, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='rider_rides',
    )
    driver = models.ForeignKey(
        RideUser, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='driver_rides',
    )
    pickup_lat = models.DecimalField(max_digits=22, decimal_places=16)
    pickup_long = models.DecimalField(max_digits=22, decimal_places=16)
    dropoff_lat = models.DecimalField(max_digits=22, decimal_places=16)
    dropoff_long = models.DecimalField(max_digits=22, decimal_places=16)
    pickup_time = models.DateTimeField()
    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.PICKUP
    )
    
    objects = models.Manager()
    recents = RecentRidesManager()


class RideEvent(models.Model):
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name='events'
    )

    description = models.CharField(max_length=100, default='')
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_description_by_status(cls, ride_status):
        descriptions = {
            Ride.StatusChoices.PICKUP: "Driver is on the way. ",
            Ride.StatusChoices.CANCELLED: "Booking is cancelled. ",
            Ride.StatusChoices.ENROUTE: "On the way to destination. ",
            Ride.StatusChoices.DROPOFF: "Arrived at destination. ",
            Ride.StatusChoices.COMPLETED: "Ride completed. ",
        }

        if ride_status not in descriptions:
            raise ValueError(f"Status '{ride_status}' does not exist. ")

        return descriptions[ride_status]