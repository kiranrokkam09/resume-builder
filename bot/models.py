from django.db import models

# Create your models here.

class Session(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at'] 
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def __str__(self):
        return self.name
    
class Chat(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="chats")
    timestamp = models.DateTimeField(auto_now_add=True) 
    message = models.TextField()
    response = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Chat"
        verbose_name_plural = "Chats"

    def __str__(self):
        return f"Chat at {self.timestamp} - Message: {self.message[:50]}"