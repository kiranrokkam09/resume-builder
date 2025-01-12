from django.db import models

# Create your models here.


class Chat(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True) 
    message = models.TextField()
    response = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Chat"
        verbose_name_plural = "Chats"

    def __str__(self):
        return f"Chat at {self.timestamp} - Message: {self.message[:50]}"