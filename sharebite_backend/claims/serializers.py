from rest_framework import serializers
from .models import Claim
from listings.serializers import FoodListingListSerializer
from accounts.serializers import UserSerializer

class ClaimSerializer(serializers.ModelSerializer):
    """Serializer for claims"""
    listing = FoodListingListSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Claim
        fields = ['id', 'listing', 'listing_id', 'receiver', 'status', 'message',
                  'pickup_time', 'created_at', 'updated_at']
        read_only_fields = ['id', 'receiver', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['receiver'] = self.context['request'].user
        return super().create(validated_data)
