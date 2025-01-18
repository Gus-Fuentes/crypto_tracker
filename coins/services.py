import requests
import ccxt
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from .models import Cryptocurrency, PriceHistory

def safe_decimal(value, default=0):
    """Convert a value to Decimal safely"""
    try:
        if value is None:
            return Decimal(default)
        return Decimal(str(float(value)))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(default)

class CryptoDataService:
    """Service for fetching and managing cryptocurrency data"""
    
    def __init__(self):
        # Initialize the Binance exchange (can be changed to other exchanges)
        self.exchange = ccxt.binance()
    
    def fetch_top_cryptocurrencies(self, limit=100):
        """Fetch top cryptocurrencies by market cap"""
        try:
            # Fetch market data from exchange
            markets = self.exchange.fetch_tickers()
            
            # Process and update each cryptocurrency
            for symbol, data in markets.items():
                if not symbol.endswith('/USDT'):  # Only process USDT pairs
                    continue
                    
                # Extract the base symbol (e.g., 'BTC' from 'BTC/USDT')
                base_symbol = symbol.split('/')[0]
                
                # Update or create cryptocurrency record
                crypto, created = Cryptocurrency.objects.update_or_create(
                    symbol=base_symbol,
                    defaults={
                        'name': base_symbol,  # Can be enhanced with a name mapping
                        'current_price': safe_decimal(data.get('last')),
                        'market_cap': safe_decimal(data.get('quoteVolume')),
                        'volume_24h': safe_decimal(data.get('baseVolume')),
                        'price_change_24h': safe_decimal(data.get('percentage')),
                        'last_updated': timezone.now(),
                    }
                )
                
                # Store historical price data
                if data.get('last'):
                    PriceHistory.objects.create(
                        cryptocurrency=crypto,
                        timestamp=timezone.now(),
                        price=safe_decimal(data['last']),
                        interval='1h'
                    )
                
            return True
        except Exception as e:
            print(f"Error fetching cryptocurrency data: [{type(e)}] {str(e)}")
            return False
    
    def fetch_historical_data(self, symbol, timeframe='1h', limit=168):
        """Fetch historical price data for a specific cryptocurrency"""
        try:
            # Fetch OHLCV data
            ohlcv = self.exchange.fetch_ohlcv(f"{symbol}/USDT", timeframe, limit=limit)
            
            crypto = Cryptocurrency.objects.get(symbol=symbol)
            
            # Store each price point
            for timestamp, open_price, high, low, close, volume in ohlcv:
                PriceHistory.objects.create(
                    cryptocurrency=crypto,
                    timestamp=timezone.datetime.fromtimestamp(timestamp/1000, tz=timezone.utc),
                    price=safe_decimal(close),
                    interval=timeframe
                )
            
            return True
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: [{type(e)}] {str(e)}")
            return False
    
    def get_price_alerts(self):
        """Get all active price alerts"""
        from .models import PriceAlert
        return PriceAlert.objects.filter(is_active=True).select_related('cryptocurrency')
    
    def check_price_alerts(self):
        """Check and process price alerts"""
        alerts = self.get_price_alerts()
        for alert in alerts:
            current_price = safe_decimal(
                self.exchange.fetch_ticker(f"{alert.cryptocurrency.symbol}/USDT").get('last')
            )
            
            if (alert.alert_type == 'above' and current_price >= alert.target_price) or \
               (alert.alert_type == 'below' and current_price <= alert.target_price):
                alert.is_active = False
                alert.triggered_at = timezone.now()
                alert.save()
                # TODO: Send notification to user

def get_top_cryptocurrencies(limit=10):
    """
    Fetch top cryptocurrencies from CoinGecko API
    
    :param limit: Number of cryptocurrencies to fetch (default 10)
    :return: List of cryptocurrency data
    """
    try:
        url = f"https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": False
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching cryptocurrency data: {e}")
        return []
