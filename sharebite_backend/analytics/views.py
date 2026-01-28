from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from .models import ImpactMetric
from .serializers import ImpactMetricSerializer
from listings.models import FoodListing
from claims.models import Claim

User = get_user_model()

class AnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for analytics and impact metrics"""
    queryset = ImpactMetric.objects.all()
    serializer_class = ImpactMetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get dashboard statistics for current user"""
        user = request.user
        
        # Calculate impact metrics from completed claims
        completed_claims = Claim.objects.filter(
            receiver=user, 
            status='completed'
        ).select_related('listing')
        
        total_meals = completed_claims.count()
        total_weight = 0
        total_carbon = 0
        
        for claim in completed_claims:
            # Extract weight from quantity (e.g., "5 kg" -> 5.0)
            try:
                quantity_str = claim.listing.quantity.lower()
                # Try to extract number from quantity string
                import re
                weight_match = re.search(r'(\d+\.?\d*)', quantity_str)
                if weight_match:
                    weight = float(weight_match.group(1))
                    # If quantity contains 'kg', use it directly; otherwise assume ~0.5kg per item
                    if 'kg' not in quantity_str:
                        weight = weight * 0.5  # Assume each item is ~0.5kg
                    total_weight += weight
                    # Calculate carbon footprint
                    carbon = ImpactMetric.calculate_carbon_footprint(
                        claim.listing.food_type, 
                        weight
                    )
                    total_carbon += carbon
            except (ValueError, AttributeError):
                # If parsing fails, use default values
                total_weight += 2.0  # Default 2kg per meal
                total_carbon += 5.0  # Default 5kg CO2 per meal
        
        # Get user-specific stats based on role
        if user.role == 'provider':
            listings_count = FoodListing.objects.filter(provider=user).count()
            completed_listings = FoodListing.objects.filter(
                provider=user, 
                status='completed'
            ).count()
            active_listings = FoodListing.objects.filter(
                provider=user, 
                status='available'
            ).count()
            
            stats = {
                'total_listings': listings_count,
                'completed_listings': completed_listings,
                'active_listings': active_listings,
            }
        else:
            claims_count = Claim.objects.filter(receiver=user).count()
            completed_claims_count = Claim.objects.filter(
                receiver=user, 
                status='completed'
            ).count()
            pending_claims = Claim.objects.filter(
                receiver=user, 
                status__in=['pending', 'confirmed']
            ).count()
            
            stats = {
                'total_claims': claims_count,
                'completed_claims': completed_claims_count,
                'pending_claims': pending_claims,
            }
        
        # Combine metrics and stats
        dashboard_data = {
            'impact': {
                'meals_saved': total_meals,
                'weight_kg': float(total_weight),
                'carbon_footprint_kg': float(total_carbon),
            },
            'stats': stats,
            'role': user.role,
        }
        
        return Response(dashboard_data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def global_impact(self, request):
        """Get global platform statistics - accessible to everyone"""
        # Calculate global impact from all completed claims
        all_completed_claims = Claim.objects.filter(
            status='completed'
        ).select_related('listing')
        
        total_meals = all_completed_claims.count()
        total_weight = 0
        total_carbon = 0
        
        for claim in all_completed_claims:
            try:
                quantity_str = claim.listing.quantity.lower()
                import re
                weight_match = re.search(r'(\d+\.?\d*)', quantity_str)
                if weight_match:
                    weight = float(weight_match.group(1))
                    if 'kg' not in quantity_str:
                        weight = weight * 0.5
                    total_weight += weight
                    carbon = ImpactMetric.calculate_carbon_footprint(
                        claim.listing.food_type, 
                        weight
                    )
                    total_carbon += carbon
            except (ValueError, AttributeError):
                total_weight += 2.0
                total_carbon += 5.0
        
        total_users = User.objects.count()
        total_listings = FoodListing.objects.count()
        completed_listings = FoodListing.objects.filter(status='completed').count()
        
        return Response({
            'total_meals_saved': total_meals,
            'total_weight_kg': float(total_weight),
            'total_carbon_reduced_kg': float(total_carbon),
            'total_users': total_users,
            'total_listings': total_listings,
            'completed_listings': completed_listings,
        })

