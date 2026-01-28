from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import FoodListing
from .serializers import FoodListingSerializer, FoodListingListSerializer

class FoodListingViewSet(viewsets.ModelViewSet):
    """ViewSet for food listings CRUD operations"""
    queryset = FoodListing.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'food_type', 'dietary_tags']
    ordering_fields = ['created_at', 'expiry_date']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FoodListingListSerializer
        return FoodListingSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by food type
        food_type = self.request.query_params.get('food_type', None)
        if food_type:
            queryset = queryset.filter(food_type=food_type)
        
        # Filter available only
        available_only = self.request.query_params.get('available_only', None)
        if available_only:
            queryset = queryset.filter(status='available', expiry_date__gt=timezone.now())
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_listings(self, request):
        """Get current user's listings"""
        listings = self.queryset.filter(provider=request.user)
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark listing as completed"""
        listing = self.get_object()
        if listing.provider != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        listing.status = 'completed'
        listing.save()
        return Response({'status': 'Listing marked as completed'})
