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
