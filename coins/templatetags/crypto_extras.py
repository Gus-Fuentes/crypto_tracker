from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def percentage(current_price, target_price):
    """Calculate the percentage progress towards the target price."""
    try:
        current = Decimal(str(current_price))
        target = Decimal(str(target_price))
        
        # If target is higher than current, show progress from 0 to target
        if target > current:
            return min((current / target) * 100, 100)
        # If target is lower than current, show progress from target to current
        else:
            return min((target / current) * 100, 100)
    except (TypeError, ValueError, ZeroDivisionError):
        return 0

@register.filter
def yesno(value, arg="yes,no"):
    """
    Given a string "yes,no", returns the first value for True and second for False.
    Example usage: {{ value|yesno:"above,below" }}
    """
    bits = arg.split(',')
    if len(bits) != 2:
        return value  # Invalid argument
    try:
        yes, no = bits
    except ValueError:
        return value  # Invalid argument
        
    return yes if value else no
