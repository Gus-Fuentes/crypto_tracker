import requests

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
