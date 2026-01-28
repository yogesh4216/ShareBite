from rest_framework import serializers
from .models import ImpactMetric

class ImpactMetricSerializer(serializers.ModelSerializer):
    """Serializer for impact metrics"""
    
    class Meta:
        model = ImpactMetric
        fields = ['id', 'user', 'listing', 'meals_saved', 'weight_kg', 
                  'carbon_footprint_kg', 'date', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
