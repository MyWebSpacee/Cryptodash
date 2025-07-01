# src/fetch_and_save.py

import pandas as pd
import logging
import json
import os
from datetime import datetime
from api.getdata import get_top_cryptos 


def fetch_crypto_data(limit=100):
    """
    Retrieves the current top cryptocurrency data from the CoinGecko API.
    Args:
    limit (int): The number of cryptocurrencies to retrieve.
    Returns:
    pd.DataFrame or None: A pandas DataFrame with the data, or None on failure.
    """
    data_df = get_top_cryptos(limit=limit)
    if data_df is None:
        logging.error(f"[{datetime.now().isoformat()}] Failed to fetch crypto data.")
        return None
    data_df['collect_timestamp'] = datetime.now().isoformat() # Added a timestamp
    return data_df

def get_save_path(data_dir='data'):
    """
    Determines the full path to the JSON file for the daily backup.
    Creates the 'data/' directory if necessary.
    Args:
    data_dir (str): The name of the directory to back up the data to.
    Returns:
    str: The full path to the file where the data should be backed up.
    """
    if not os.path.exists(data_dir):
        os.makedirs(data_dir) 
    file_name = datetime.now().strftime('crypto_data_%Y-%m-%d.json')
    file_path = os.path.join(data_dir, file_name)
    return file_path

def save_data_to_json(data_df: pd.DataFrame, file_path: str):
    """
    Saves a pandas DataFrame to a JSON file.
    Args:
    data_df (pd.DataFrame): The DataFrame to save.
    file_path (str): The full path to the JSON file.
    """
    if data_df.empty:
        return

    data_to_save = data_df.to_dict(orient='records')
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)
        logging.info(f"[{datetime.now().isoformat()}] Data saved to : {file_path}")
    except IOError as e:
        logging.error(f"[{datetime.now().isoformat()}] Failed to save data to {file_path}: {e}")

def main_save_daily_crypto_data():
    """
    Main function to orchestrate daily recovery and backup
    """
    crypto_data = fetch_crypto_data(limit=100) 
    if crypto_data is None:
        return

    file_path = get_save_path()
    save_data_to_json(crypto_data, file_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main_save_daily_crypto_data()