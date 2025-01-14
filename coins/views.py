from django.shortcuts import render
from .services import get_top_cryptocurrencies

# Create your views here.

def crypto_list(request):
    """
    View to display top cryptocurrencies
    """
    cryptocurrencies = get_top_cryptocurrencies()
    return render(request, 'coins/crypto_list.html', {
        'cryptocurrencies': cryptocurrencies
    })
