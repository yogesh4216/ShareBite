from django.db import models
from django.conf import settings

class FoodListing(models.Model):
    """Food listing model for surplus food items"""
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('claimed', 'Claimed'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]
    
    FOOD_TYPE_CHOICES = [
        ('prepared', 'Prepared Food'),
        ('packaged', 'Packaged Goods'),
        ('produce', 'Fresh Produce'),
        ('dairy', 'Dairy Products'),
        ('bakery', 'Bakery Items'),
        ('other', 'Other'),
    ]
    
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    food_type = models.CharField(max_length=20, choices=FOOD_TYPE_CHOICES, default='other')
    phone_number = models.CharField(max_length=20, help_text="Contact number for pickup coordination")
    quantity = models.CharField(max_length=100, help_text="e.g., '5 plates', '2 kg', '10 items'")
    expiry_date = models.DateTimeField()
    pickup_location = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    image = models.ImageField(upload_to='listings/', blank=True, null=True)
    dietary_tags = models.CharField(max_length=255, blank=True, help_text="e.g., 'vegetarian, gluten-free'")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'expiry_date']),
            models.Index(fields=['food_type']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.provider.username}"
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expiry_date
