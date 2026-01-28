from django.db import models
from django.conf import settings

class Notification(models.Model):
    """Notification log model to track sent messages"""
    
    TYPE_CHOICES = [
        ('claim_created', 'Claim Created'),
        ('claim_confirmed', 'Claim Confirmed'),
        ('pickup_reminder', 'Pickup Reminder'),
        ('expiry_alert', 'Expiry Alert'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    phone_number = models.CharField(max_length=20)
    sent_successfully = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.user.username}"
