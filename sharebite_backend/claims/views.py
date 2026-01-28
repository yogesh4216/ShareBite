from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Claim
from .serializers import ClaimSerializer
from listings.models import FoodListing

class ClaimViewSet(viewsets.ModelViewSet):
    """ViewSet for claim operations"""
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Optimize with select_related to reduce database queries
        queryset = super().get_queryset().select_related('listing', 'receiver', 'listing__provider')
        
        # Filter by user role
        user = self.request.user
        if user.role == 'provider':
            # Show claims for provider's listings
            queryset = queryset.filter(listing__provider=user)
        else:
            # Show user's own claims
            queryset = queryset.filter(receiver=user)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create a new claim"""
        import time
        start_time = time.time()
        
        listing_id = request.data.get('listing_id')
        
        # Optimize query with select_related to reduce database hits
        try:
            listing = FoodListing.objects.select_related('provider').get(id=listing_id)
        except FoodListing.DoesNotExist:
            return Response({'error': 'Listing not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Check if listing is available
        if listing.status != 'available':
            return Response({'error': 'Listing is not available'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already claimed this listing (idempotency)
        existing_claim = Claim.objects.filter(
            listing=listing, 
            receiver=request.user
        ).first()
        
        if existing_claim:
            # Return existing claim instead of error for idempotency
            serializer = self.get_serializer(existing_claim)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        claim = serializer.save()
        
        # Update listing status
        listing.status = 'claimed'
        listing.save(update_fields=['status'])
        
        elapsed_time = time.time() - start_time
        print(f"✅ Claim created in {elapsed_time:.2f}s for listing {listing_id} by user {request.user.username}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a claim (provider only)"""
        claim = self.get_object()
        if claim.listing.provider != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        claim.status = 'confirmed'
        claim.save()
        return Response({'status': 'Claim confirmed'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark claim as completed"""
        claim = self.get_object()
        claim.status = 'completed'
        claim.save()
        
        # Update listing status
        claim.listing.status = 'completed'
        claim.listing.save()
        
        return Response({'status': 'Claim completed'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a claim"""
        claim = self.get_object()
        if claim.receiver != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        claim.status = 'cancelled'
        claim.save()
        
        # Revert listing status if no other active claims
        if not claim.listing.claims.filter(status__in=['pending', 'confirmed']).exists():
            claim.listing.status = 'available'
            claim.listing.save()
        
        return Response({'status': 'Claim cancelled'})
