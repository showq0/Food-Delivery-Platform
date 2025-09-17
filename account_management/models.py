from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    CUSTOMER = 'customer'
    DRIVER = 'driver'
    AGENT = 'agent'
    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (DRIVER, 'Driver'),
        (AGENT, 'Agent'),
    ]
    role = models.CharField(
        max_length=8,
        choices=ROLE_CHOICES,
        blank=True,
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    payment_info = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.username}"
