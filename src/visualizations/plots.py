# src/visualizations/plots.py

import pandas as pd
import plotly.graph_objects as go
import logging
import os
import json
from datetime import datetime, timedelta # Importe timedelta for date calculations


def load_historical_data(data_dir='data'):
    """
    charge every JSON file that starts with 'crypto_data_' and ends with '.json' in the directory.
    normalizes the date to the start of the day
    Arg 
       data_dir: The directory where the JSON files are stored.
    Returns:
        pd.DataFrame: A DataFrame containing the loaded data if available, otherwise an empty DataFrame.
    """
    all_data = []
    if not os.path.exists(data_dir):
        return pd.DataFrame()

    for filename in sorted(os.listdir(data_dir)):
        if filename.startswith('crypto_data_') and filename.endswith('.json'):
            file_path = os.path.join(data_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not data:
                        logging.warning(f"[{datetime.now().isoformat()}] file {filename} does not contain any data or incorrectly formatted.")
                        continue

                    for record in data:
                        try:
                                # Normalize the date to the start of the day using the timestamp
                                record['date_processed'] = pd.to_datetime(record.get('collect_timestamp')).normalize()
                        except ValueError:
                                # If 'collect_timestamp' is not available or invalid, use the filename as a fallback
                                record['date_processed'] = pd.to_datetime(filename.replace('crypto_data_', '').replace('.json', ''), errors='coerce').normalize()
                        
                        if pd.isna(record['date_processed']):
                            logging.warning(f"[{datetime.now().isoformat()}] Problem with file {filename} or timestamp.") 
                            continue
                    all_data.extend(data)
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"[{datetime.now().isoformat()}] Error loading data from {file_path}: {e}")
                continue
    
    if not all_data:
        return pd.DataFrame()

    df = pd.DataFrame(all_data)
    df['date'] = pd.to_datetime(df['date_processed'], errors='coerce')
    df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce')
    df = df.dropna(subset=['current_price', 'date'])
    
    return df.sort_values(by=['date', 'name'])


def plot_price_evolution_with_moving_averages(df: pd.DataFrame, crypto_id: str, time_period: str = 'Tout'):
    """
    Generates a chart of a cryptocurrency's price evolution using moving averages,
    filtered by a given time period.

    Args:
    df(pd.DataFrame): DataFrame containing consolidated historical data.
    crypto_id(str): The ID of the cryptocurrency to display (e.g., 'bitcoin').
    time_period(str): The time period to filter on ('24h', '7d', '1m', '1y', 'All').

    Returns:
    go.Figure: A Plotly figure.
    """
    crypto_df = df[df['id'] == crypto_id].copy()
    
    if crypto_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text=f" No data found for {crypto_id}",
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=20, color="gray")
        )
        fig.update_layout(title=f"Price Evolution for {crypto_id.capitalize()}")
        return fig

    # filtring by date based on the selected time period
    end_date = crypto_df['date'].max() # recent date in the data
    start_date = None

    if time_period == '7d':
        start_date = end_date - timedelta(days=7)
    elif time_period == '1m': # 30 days 
        start_date = end_date - timedelta(days=30)
    elif time_period == '1y': # 365 days
        start_date = end_date - timedelta(days=365)
    # 'all' mean no filtering

    if start_date:
        crypto_df = crypto_df[crypto_df['date'] >= start_date]

    # group by date to ensure we have one entry per day
    crypto_df = crypto_df.sort_values(by='date')
    
    # Calculate the average price for each day   
    daily_prices = crypto_df.groupby('date')['current_price'].mean().reset_index()
    daily_prices['date_for_plot'] = daily_prices['date'] # Use 'date' for plotting

    if daily_prices.empty or len(daily_prices['date_for_plot'].unique()) <= 1 :
         fig = go.Figure()
         fig.add_annotation(
            text=f"No data found for {crypto_id}.",
            xref="paper", yref="paper", showarrow=False, font=dict(size=16, color="gray")
         )
         fig.update_layout(title=f"Price Evolution for {crypto_id.capitalize()} ({time_period})")
         return fig


    # Using rolling mean to calculate the moving averages
    daily_prices['MA_7J'] = daily_prices['current_price'].rolling(window=7, min_periods=1).mean() # min_periods for short data
    daily_prices['MA_30J'] = daily_prices['current_price'].rolling(window=30, min_periods=1).mean()


    fig = go.Figure()

    # Curent price trace
    fig.add_trace(go.Scatter(
        x=daily_prices['date_for_plot'],
        y=daily_prices['current_price'],
        mode='lines',
        name='Current Price',
        line=dict(color='blue')
    ))

    # adding the moving averages to the plot
    if len(daily_prices) >= 7: # No MA if less than 7 days
        fig.add_trace(go.Scatter(
            x=daily_prices['date_for_plot'],
            y=daily_prices['MA_7J'],
            mode='lines',
            name='7 Days Moving Average',
            line=dict(color='orange', dash='dot')
        ))

    # adding the 30 days moving average to the plot
    if len(daily_prices) >= 30: # No MA if less than 30 days
        fig.add_trace(go.Scatter(
            x=daily_prices['date_for_plot'],
            y=daily_prices['MA_30J'],
            mode='lines',
            name='30 Days Moving Average',
            line=dict(color='red', dash='dash')
        ))

    # Adding the layout and formatting
    fig.update_layout(
        title=f"Price Evolution for {crypto_id.capitalize()} ({time_period})",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

