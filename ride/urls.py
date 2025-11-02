from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API for Ride
    path('api/', include('api.urls')),

    # Authenticate users through auth tokens
    path('api/login/', TokenObtainPairView.as_view(), name='access_token'),
    path('api/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]
