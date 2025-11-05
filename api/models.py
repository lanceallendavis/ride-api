from django.db import models
from django.contrib.auth.models import AbstractUser


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
        BOOKED = 'BK', 'Booked'
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
        default=StatusChoices.BOOKED
    )






    



