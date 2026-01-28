from rest_framework import serializers
from .models import FoodListing
from accounts.serializers import UserSerializer

class FoodListingSerializer(serializers.ModelSerializer):
    """Serializer for food listings"""
    provider = UserSerializer(read_only=True)
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = FoodListing
        fields = ['id', 'provider', 'title', 'description', 'food_type', 'quantity', 'phone_number',
                  'expiry_date', 'pickup_location', 'latitude', 'longitude', 'image',
                  'dietary_tags', 'status', 'is_expired', 'created_at', 'updated_at']
        read_only_fields = ['id', 'provider', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['provider'] = self.context['request'].user
        return super().create(validated_data)


class FoodListingListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing views"""
    provider_name = serializers.CharField(source='provider.username', read_only=True)
    
    class Meta:
        model = FoodListing
        fields = ['id', 'title', 'food_type', 'quantity', 'phone_number', 'expiry_date', 
                  'pickup_location', 'status', 'provider_name', 'created_at']
