from django.urls import path
from .views.main_views import (
    home,
    cryptocurrency_detail,
    watchlist,
    alerts,
    create_price_alert,
    get_historical_data,
    delete_alert
)
from .views.auth_views import login_view, register_view, logout_view

app_name = 'coins'

urlpatterns = [
    # Web views
    path('', home, name='home'),
    path('crypto/<str:symbol>/', cryptocurrency_detail, name='crypto_detail'),
    path('watchlist/', watchlist, name='watchlist'),
    path('alerts/', alerts, name='alerts'),
    
    # Authentication
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # API endpoints
    path('api/alerts/create/<str:symbol>/', create_price_alert, name='create_alert'),
    path('api/historical/<str:symbol>/', get_historical_data, name='historical_data'),
    path('api/alerts/<int:alert_id>/delete/', delete_alert, name='delete_alert'),
]
