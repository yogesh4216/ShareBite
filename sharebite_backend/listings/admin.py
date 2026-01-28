from django.contrib import admin
from .models import FoodListing

@admin.register(FoodListing)
class FoodListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'provider', 'food_type', 'status', 'expiry_date', 'created_at']
    list_filter = ['status', 'food_type']
    search_fields = ['title', 'description']
