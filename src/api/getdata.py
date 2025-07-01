import requests
import pandas as pd
import logging

def get_top_cryptos(vs_currency='usd', limit=10, page=1):
    """
    Retrieve the top cryptocurrencies by market cap from Coingecko API.
    Args:
        vs_currency (str): The currency to compare against (default is 'usd').
        limit (int): The number of cryptocurrencies to retrieve (default is 10).
        page (int): The page number for pagination (default is 1).
    Returns:
        pd.DataFrame : A pandas DataFrame containing cryptocurrency data.
        None: If the request fails or no data is returned.
    """
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={vs_currency}&order=market_cap_desc&per_page={limit}&page={page}&sparkline=false"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        if data :
            df = pd.DataFrame(data)
            df = df[['id', 'symbol', 'name', 'current_price', 'market_cap','market_cap_change_percentage_24h' , 'total_volume', 'price_change_percentage_24h', 'image', 'low_24h', 'high_24h']]
            return df
        else :
            logging.info("no data found.")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from the API: {e}")
        return None
    