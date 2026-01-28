from django.http import JsonResponse
from django.views import View

class WelcomeView(View):
    """Welcome page with API information"""
    
    def get(self, request):
        return JsonResponse({
            'message': 'Welcome to ShareBite API',
            'version': '1.0',
            'documentation': {
                'swagger': request.build_absolute_uri('/api/docs/'),
                'redoc': request.build_absolute_uri('/api/redoc/'),
            },
            'endpoints': {
                'authentication': {
                    'register': '/api/auth/register/',
                    'login': '/api/auth/login/',
                    'refresh': '/api/auth/refresh/',
                    'profile': '/api/auth/profile/',
                },
                'listings': '/api/listings/',
                'claims': '/api/claims/',
                'analytics': '/api/analytics/',
            },
            'admin': request.build_absolute_uri('/admin/'),
        })

def setup_demo_data(request):
    """
    Temporary endpoint to seed database for hackathon demo.
    Run by visiting /setup_demo_data/
    """
    from accounts.models import User
    from listings.models import Listing
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # 1. Create Provider
    try:
        provider = User.objects.get(username='demo_provider')
    except User.DoesNotExist:
        provider = User.objects.create_user(
            username='demo_provider', 
            email='provider@sharebite.com', 
            password='demo123', 
            role='provider', 
            first_name='Pizza', 
            last_name='Place'
        )
        
    # 2. Create Receiver
    try:
        receiver = User.objects.get(username='demo_receiver')
    except User.DoesNotExist:
        receiver = User.objects.create_user(
            username='demo_receiver', 
            email='receiver@sharebite.com', 
            password='demo123', 
            role='receiver', 
            first_name='John', 
            last_name='Doe'
        )

    # 3. Create Admin
    try:
        User.objects.get(username='demo_admin')
    except User.DoesNotExist:
        User.objects.create_superuser('demo_admin', 'admin@example.com', 'Demo123!')

    # 4. Create Sample Listing
    if not Listing.objects.filter(title='Fresh Pizza - 3 Slices').exists():
        Listing.objects.create(
            title='Fresh Pizza - 3 Slices',
            food_type='prepared',
            quantity='3 slices',
            pickup_location='123 Main St, New York, NY',
            provider=provider,
            expiry_date=timezone.now() + timedelta(hours=4),
            description="Fresh pepperoni pizza slices left over from lunch service."
        )

    return JsonResponse({'status': 'success', 'message': 'Demo data created!'})
