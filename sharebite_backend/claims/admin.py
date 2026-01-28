from django.contrib import admin
from .models import Claim

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['listing', 'receiver', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['listing__title', 'receiver__username']
