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
