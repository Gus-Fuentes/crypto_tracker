from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Cryptocurrency, Watchlist, PriceAlert
from ..serializers import CryptocurrencySerializer, WatchlistSerializer, PriceAlertSerializer
from ..services import CryptoDataService

class CryptocurrencyViewSet(viewsets.ModelViewSet):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer

class WatchlistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchlistSerializer
    
    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

class PriceAlertViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PriceAlertSerializer
    
    def get_queryset(self):
        return PriceAlert.objects.filter(user=self.request.user)

def home(request):
    crypto_service = CryptoDataService()
    
    # Get cached cryptocurrency data
    all_cryptos = crypto_service.get_cached_data()
    if not all_cryptos:
        # If no cached data, fetch it
        all_cryptos = crypto_service.fetch_top_cryptocurrencies()
        if not all_cryptos:
            all_cryptos = Cryptocurrency.objects.all()
    
    # Sort by market cap and get top 10
    cryptocurrencies = sorted(all_cryptos, key=lambda x: x.market_cap or 0, reverse=True)[:10]
    
    # Calculate market statistics
    total_market_cap = sum(c.market_cap or 0 for c in all_cryptos)
    total_volume_24h = sum(c.volume_24h or 0 for c in all_cryptos)
    
    # Calculate BTC dominance
    btc = next((c for c in all_cryptos if c.symbol == 'BTC'), None)
    btc_dominance = (btc.market_cap / total_market_cap * 100) if btc and total_market_cap > 0 else 0
    
    # Get watchlist symbols for the current user
    watchlist_symbols = []
    if request.user.is_authenticated:
        watchlist_symbols = list(Watchlist.objects.filter(
            user=request.user,
            is_active=True
        ).values_list('cryptocurrency__symbol', flat=True))
    
    context = {
        'cryptocurrencies': cryptocurrencies,
        'total_market_cap': total_market_cap,
        'total_volume_24h': total_volume_24h,
        'btc_dominance': btc_dominance,
        'watchlist_symbols': watchlist_symbols,
    }
    
    return render(request, 'coins/home.html', context)

def cryptocurrency_detail(request, symbol):
    crypto = get_object_or_404(Cryptocurrency, symbol=symbol.upper())
    crypto_service = CryptoDataService()
    
    # Fetch latest data for the cryptocurrency
    crypto_service.fetch_historical_data(symbol)
    
    # Get historical data from database
    historical_data = crypto.price_history.all().order_by('-timestamp')[:168]  # Last 7 days of hourly data
    
    return render(request, 'coins/detail.html', {
        'crypto': crypto,
        'historical_data': historical_data
    })

@login_required
def watchlist(request):
    watchlist_items = Watchlist.objects.select_related('cryptocurrency').filter(user=request.user)
    return render(request, 'coins/watchlist.html', {'watchlist': watchlist_items})

@login_required
def alerts(request):
    active_alerts = PriceAlert.objects.select_related('cryptocurrency').filter(user=request.user, is_active=True)
    triggered_alerts = PriceAlert.objects.select_related('cryptocurrency').filter(user=request.user, is_active=False)
    
    return render(request, 'coins/alerts.html', {
        'active_alerts': active_alerts,
        'triggered_alerts': triggered_alerts,
        'alerts': list(active_alerts) + list(triggered_alerts)
    })

@login_required
def toggle_watchlist(request, symbol):
    """
    Toggle a cryptocurrency's watchlist status for the current user.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        crypto = get_object_or_404(Cryptocurrency, symbol=symbol.upper())
        
        # Try to get existing watchlist item
        try:
            watchlist_item = Watchlist.objects.get(
                cryptocurrency=crypto,
                user=request.user
            )
            # Toggle the active status
            watchlist_item.is_active = not watchlist_item.is_active
            watchlist_item.save()
        except Watchlist.DoesNotExist:
            # Create new watchlist item
            watchlist_item = Watchlist.objects.create(
                cryptocurrency=crypto,
                user=request.user,
                is_active=True
            )
        
        return JsonResponse({
            'status': 'added' if watchlist_item.is_active else 'removed',
            'symbol': symbol
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)

@login_required
def create_price_alert(request, symbol):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    crypto = get_object_or_404(Cryptocurrency, symbol=symbol.upper())
    alert_type = request.POST.get('alert_type')
    target_price = float(request.POST.get('target_price'))
    
    alert = PriceAlert.objects.create(
        user=request.user,
        cryptocurrency=crypto,
        alert_type=alert_type,
        target_price=target_price,
        is_active=True
    )
    
    return JsonResponse({
        'status': 'success',
        'alert_id': alert.id
    })

@login_required
def delete_alert(request, alert_id):
    alert = get_object_or_404(PriceAlert, id=alert_id, user=request.user)
    alert.delete()
    return JsonResponse({'status': 'success'})

def get_historical_data(request, symbol):
    crypto = get_object_or_404(Cryptocurrency, symbol=symbol.upper())
    historical_data = crypto.price_history.all().order_by('-timestamp')[:168]
    
    data = [{
        'timestamp': entry.timestamp.isoformat(),
        'price': float(entry.price)
    } for entry in historical_data]
    
    return JsonResponse({'data': data})
