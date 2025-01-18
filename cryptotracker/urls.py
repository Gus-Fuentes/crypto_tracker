"""
URL configuration for cryptotracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from coins.views import (
    CryptocurrencyViewSet,
    WatchlistViewSet,
    PriceAlertViewSet
)
from coins.views.main_views import toggle_watchlist

# Create a router for our API
router = routers.DefaultRouter()
router.register(r'cryptocurrencies', CryptocurrencyViewSet, basename='cryptocurrency')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'alerts', PriceAlertViewSet, basename='alert')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('coins.urls')),
    path('api/', include(router.urls)),
    path('api/watchlist/toggle/<str:symbol>/', toggle_watchlist, name='toggle_watchlist'),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'coins.views.error_views.handler404'
handler500 = 'coins.views.error_views.handler500'
