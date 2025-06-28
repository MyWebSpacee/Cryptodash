import pandas as pd
import json
import os
from datetime import datetime
from src.api.coingecko import get_top_cryptos

def save_historical_data_to_json():
    """
    Save historical stock data to a timestamped JSON file in the data/ folder.
    """
    print("Recuperation des donnees historiques des cryptomonnaies...")
    # Get historical data from Coingecko API
    historical_data_df = get_top_cryptos(limit=100) # Adjust limit as needed
    if historical_data_df is None:
        print("Echec de la recuperation des donnees historiques des cryptomonnaies. Arret de la sauvegarde.")
        return
    # add a new column 'timestamp' with the current date and time in ISO
    historical_data_df['timestamp'] = datetime.now().isoformat()
    # prepare the save path if it does not exist
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    # file name with timestamp
    file_name = datetime.now().strftime('crypto_data_%Y-%m-%d.json')
    file_path = os.path.join(data_dir, file_name)
    #Load existing data if available
    existing_data = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r' , encoding='utf-8') as file:
                existing_data = json.load(file)
                print(f"Chargement des donnees existantes depuis {file_path}")
        except json.JSONDecodeError:
            print(f"Erreur de decodage JSON dans le fichier {file_path}. Un nouveau fichier sera cree.")
            existing_data = []
    #convert DataFrame to a list of dictionaries and append the new data
    new_data = historical_data_df.to_dict(orient='records')
    existing_data.extend(new_data)
    # Save the updated data to the JSON file
    try: 
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)
        print(f"Les donnees historiques des cryptomonnaies ont ete sauvegardees dans {file_path}")
    except IOError as e:
        print(f"Erreur lors de la sauvegarde des donnees dans {file_path}: {e}")



if __name__ == "__main__":
    save_historical_data_to_json()