from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .views import WelcomeView, setup_demo_data
from accounts.views import RegisterView, LoginView, ProfileView
from listings.views import FoodListingViewSet
from claims.views import ClaimViewSet
from analytics.views import AnalyticsViewSet

# API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="ShareBite API",
        default_version='v1',
        description="Food Waste Reduction Platform API",
        contact=openapi.Contact(email="contact@sharebite.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Router for ViewSets
router = DefaultRouter()
router.register(r'listings', FoodListingViewSet, basename='listing')
router.register(r'claims', ClaimViewSet, basename='claim')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    # Root - Welcome page with API info
    path('', WelcomeView.as_view(), name='index'),
    path('setup_demo_data/', setup_demo_data, name='setup_demo_data'),
    
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Authentication
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', ProfileView.as_view(), name='profile'),
    
    # API Routes
    path('api/', include(router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
