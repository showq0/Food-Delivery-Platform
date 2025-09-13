from django.db import models
from account_management.models import User
from dirtyfields import DirtyFieldsMixin

# Create your models here.


class Order(DirtyFieldsMixin, models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('picked_up', 'Picked up'),
        ('delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

    def __str__(self):
        return f"Order {self.id} for {self.customer.username} - {self.status}"
