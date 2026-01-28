from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model with role-based types"""
    
    ROLE_CHOICES = [
        ('provider', 'Provider'),
        ('receiver', 'Receiver'),
        ('ngo', 'NGO'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receiver')
    phone_number = models.CharField(max_length=20, blank=True)
    organization_name = models.CharField(max_length=255, blank=True, help_text="For NGOs and businesses")
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
