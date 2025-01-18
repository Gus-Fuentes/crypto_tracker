from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Cryptocurrency(models.Model):
    """
    Model to store cryptocurrency information.
    This is the main model that holds current market data for each cryptocurrency.
    """
    # Unique identifier for the cryptocurrency (e.g., 'BTC', 'ETH')
    symbol = models.CharField(max_length=10, unique=True)
    # Full name of the cryptocurrency (e.g., 'Bitcoin', 'Ethereum')
    name = models.CharField(max_length=100)
    # Current price with 8 decimal places to handle small-value cryptocurrencies
    current_price = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    # Market capitalization in USD
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    # 24-hour trading volume in USD
    volume_24h = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    # 24-hour price change percentage
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Timestamp of the last data update
    last_updated = models.DateTimeField(auto_now=True)
    # URL to the cryptocurrency's logo/icon
    image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        verbose_name_plural = "cryptocurrencies"
        ordering = ['-market_cap']  # Order by market cap descending by default

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class Watchlist(models.Model):
    """
    Model to track which cryptocurrencies a user is watching.
    Allows users to create a personalized list of cryptocurrencies they're interested in.
    """
    # Link to the Django user model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Link to the cryptocurrency being watched
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    # When the cryptocurrency was added to the watchlist
    added_at = models.DateTimeField(auto_now_add=True)
    # Whether the watchlist item is active
    is_active = models.BooleanField(default=True)

    class Meta:
        # Ensure a user can't add the same cryptocurrency twice
        unique_together = ('user', 'cryptocurrency')

    def __str__(self):
        return f"{self.user.username}'s watchlist - {self.cryptocurrency.symbol}"

class PriceAlert(models.Model):
    """
    Model to manage price alerts for cryptocurrencies.
    Users can set alerts to be notified when a cryptocurrency reaches a certain price.
    """
    # Define the types of alerts available
    ALERT_TYPES = [
        ('above', 'Price Above'),
        ('below', 'Price Below'),
    ]

    # Link to the user who created the alert
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Link to the cryptocurrency being tracked
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    # Whether to trigger alert when price goes above or below target
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPES)
    # The price at which to trigger the alert
    target_price = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        validators=[MinValueValidator(Decimal('0.00000001'))]  # Minimum value of 1 satoshi
    )
    # Whether the alert is currently active
    is_active = models.BooleanField(default=True)
    # When the alert was created
    created_at = models.DateTimeField(auto_now_add=True)
    # When the alert was triggered (if it has been)
    triggered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.cryptocurrency.symbol} {self.alert_type} {self.target_price}"

class PriceHistory(models.Model):
    """
    Model to store historical price data for cryptocurrencies.
    Maintains price history at different intervals for charting and analysis.
    """
    # Available time intervals for historical data
    INTERVALS = [
        ('1h', '1 Hour'),
        ('24h', '24 Hours'),
        ('7d', '7 Days'),
        ('30d', '30 Days'),
    ]

    # Link to the cryptocurrency
    cryptocurrency = models.ForeignKey(
        Cryptocurrency,
        on_delete=models.CASCADE,
        related_name='price_history'
    )
    # Timestamp of the price data point
    timestamp = models.DateTimeField()
    # Price at this point in time
    price = models.DecimalField(max_digits=20, decimal_places=8)
    # Time interval this data point represents
    interval = models.CharField(max_length=3, choices=INTERVALS)

    class Meta:
        verbose_name_plural = "price histories"
        ordering = ['-timestamp']  # Most recent first
        indexes = [
            models.Index(fields=['cryptocurrency', '-timestamp']),
            models.Index(fields=['interval', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.cryptocurrency.symbol} - {self.price} at {self.timestamp}"
