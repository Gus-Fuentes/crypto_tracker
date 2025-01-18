from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cryptocurrency, Watchlist, PriceAlert, PriceHistory

class CryptocurrencySerializer(serializers.ModelSerializer):
    """Serializer for cryptocurrency data"""
    class Meta:
        model = Cryptocurrency
        fields = '__all__'

class WatchlistSerializer(serializers.ModelSerializer):
    """Serializer for user watchlists"""
    cryptocurrency_details = CryptocurrencySerializer(source='cryptocurrency', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Watchlist
        fields = ['id', 'user', 'cryptocurrency', 'cryptocurrency_details', 'added_at', 'is_active']
        read_only_fields = ['added_at']

class PriceAlertSerializer(serializers.ModelSerializer):
    """Serializer for price alerts"""
    cryptocurrency_details = CryptocurrencySerializer(source='cryptocurrency', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PriceAlert
        fields = ['id', 'user', 'cryptocurrency', 'cryptocurrency_details', 'alert_type', 
                 'target_price', 'is_active', 'created_at', 'triggered_at']
        read_only_fields = ['created_at', 'triggered_at']

class PriceHistorySerializer(serializers.ModelSerializer):
    """Serializer for historical price data"""
    class Meta:
        model = PriceHistory
        fields = ['timestamp', 'price', 'interval']
