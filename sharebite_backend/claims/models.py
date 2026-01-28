from django.db import models
from django.conf import settings
from listings.models import FoodListing

class Claim(models.Model):
    """Claim/request model linking receivers to food listings"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    listing = models.ForeignKey(FoodListing, on_delete=models.CASCADE, related_name='claims')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='claims')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text="Optional message to provider")
    pickup_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['listing', 'receiver']
    
    def __str__(self):
        return f"Claim by {self.receiver.username} for {self.listing.title}"
