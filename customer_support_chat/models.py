from django.db import models
from account_management.models import User


# Create your models here.

class Chat(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_chats',
                                 limit_choices_to={'role': 'customer'})
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_chats',
                              limit_choices_to={'role': 'agent'})
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['agent', 'customer']

    def __str__(self):
        return f"Chat {self.id} between {self.customer.username} and {self.agent.username}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['content']

    def __str__(self):
        return f"{self.content}"
