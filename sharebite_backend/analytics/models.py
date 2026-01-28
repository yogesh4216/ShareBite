from django.db import models
from django.conf import settings
from listings.models import FoodListing

class ImpactMetric(models.Model):
    """Model to track meals saved and carbon footprint"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='impact_metrics')
    listing = models.ForeignKey(FoodListing, on_delete=models.CASCADE, related_name='impact_metrics', null=True, blank=True)
    meals_saved = models.IntegerField(default=0)
    weight_kg = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    carbon_footprint_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="CO2 equivalent in kg")
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Impact for {self.user.username} - {self.meals_saved} meals"
    
    @staticmethod
    def calculate_carbon_footprint(food_type, weight_kg):
        """Calculate carbon footprint based on food type and weight"""
        # Average CO2 emissions per kg of food (simplified)
        carbon_factors = {
            'prepared': 2.5,
            'packaged': 1.8,
            'produce': 0.9,
            'dairy': 3.2,
            'bakery': 1.5,
            'other': 2.0,
        }
        factor = carbon_factors.get(food_type, 2.0)
        return float(weight_kg) * factor
