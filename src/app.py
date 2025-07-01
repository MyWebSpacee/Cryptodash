# src/app.py

import streamlit as st
import pandas as pd
import os
import sys
# --- environment config ---

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
    print(f"DEBUG: Added {project_root} to sys.path")

# Module imports
from api.getdata import get_top_cryptos
from src.visualizations.plots import load_historical_data, plot_price_evolution_with_moving_averages

# --- streamlit config ---
st.set_page_config(
    page_title="CryptoDashboard by OpenInsight Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Cache functions ---
@st.cache_data(ttl=3600)
def get_historical_data_cached():
    return load_historical_data()

@st.cache_data(ttl=60)
def get_realtime_data_cached():
    return get_top_cryptos(limit=100) 

# --- Utility function for handling missing values and formatting ---
# --- New formatting function for metrics (with HTML) ---
# --- Cache and format_value functions  ---
def format_metric_value(value, prefix="", suffix="", decimals=2):
    """Formats a value for metrics, including HTML."""
    if pd.isna(value):
        return "N/A"
    if isinstance(value, (int, float)):
        if suffix == "%":
            color = "green" if value >= 0 else "red"
            return f"<span style='color:{color}'>{prefix}{value:,.{decimals}f}{suffix}</span>"
        return f"{prefix}{value:,.{decimals}f}{suffix}"
    return str(value)

def format_dataframe_value(value, prefix="", suffix="", decimals=2):
    """Formats a value for dataframes, without HTML."""
    if pd.isna(value):
        return "N/A"
    if isinstance(value, (int, float)):
        return f"{prefix}{value:,.{decimals}f}{suffix}"
    return str(value)


# --- Header and Refresh Button on the same line (unchanged) ---
title_col, refresh_btn_col = st.columns([0.7, 0.3])

with title_col:
    st.markdown("## CryptoDashboard")

with refresh_btn_col:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Refresh data", help="Update the data from the API"):
        st.cache_data.clear()
        st.rerun()
st.markdown("---")

# --- NAVIGATION ---
st.sidebar.header("Navigation 🧭")

historical_df = get_historical_data_cached()
realtime_df = get_realtime_data_cached()

if historical_df.empty:
    st.sidebar.warning("Loading historical data in progress...")
    selected_crypto_name = None
    selected_crypto_id = None
else:
    available_cryptos = sorted(historical_df['name'].unique())
    crypto_name_to_id = historical_df[['name', 'id']].drop_duplicates().set_index('name')['id'].to_dict()

    selected_crypto_name = st.sidebar.selectbox(
        "Select a cryptocurrency:",
        options=available_cryptos,
        index=available_cryptos.index('Bitcoin') if 'Bitcoin' in available_cryptos else 0
    )
    selected_crypto_id = crypto_name_to_id.get(selected_crypto_name)

st.sidebar.markdown("---")

st.sidebar.header("Resources 📚")
st.sidebar.markdown(
    "[API Documentation](https://www.coingecko.com/api/documentation)"
)


# --- MAIN STRUCTURE IN 3 COLUMNS ---
col_left, col_center, col_right = st.columns([0.2, 0.55, 0.25])

# --- LEFT COLUMN: Key Indicators (Selected Crypto) and TIME FILTERS ---
with col_left:
    st.subheader("Key Indicators (24h)")
    if realtime_df is not None and not realtime_df.empty and selected_crypto_id:
        selected_crypto_data_series = realtime_df[realtime_df['id'] == selected_crypto_id].iloc[0]
        
        st.markdown(f"**For {selected_crypto_data_series.get('name', 'N/A')} ({selected_crypto_data_series.get('symbol', 'N/A').upper()}):**")
        
        with st.container(border=True):
            st.metric(label="Current Price", value=format_metric_value(selected_crypto_data_series.get('current_price'), prefix="$ ", decimals=4))
        
        with st.container(border=True):
            st.markdown(f"**24h Change**: {format_metric_value(selected_crypto_data_series.get('price_change_percentage_24h'), suffix='%', decimals=2)}", unsafe_allow_html=True)

        with st.container(border=True):
            st.metric(label="24h Trading Volume", value=format_metric_value(selected_crypto_data_series.get('total_volume'), prefix="$ ", decimals=0))
        
        with st.container(border=True):
            st.metric(label="Market Cap", value=format_metric_value(selected_crypto_data_series.get('market_cap'), prefix="$ ", decimals=0))

    else:
        st.info("Select a cryptocurrency or wait for the data to load.")
    
    st.markdown("---")
    st.subheader("Chart Filter")
    
    # --- Time filter buttons ---
    time_periods = ['7d', '1m', '1y', 'All']
    # Use st.radio or st.button in columns for buttons
    selected_time_period = st.radio(
        "Show history for:",
        options=time_periods,
        index=3, # 'All' is selected by default
        horizontal=True # Display buttons in a row
    )
    # Store the selected period in Streamlit state for reuse
    st.session_state.selected_time_period = selected_time_period
    # --- End of time filter buttons ---


# --- CENTER COLUMN: Price Evolution Chart + Detailed Info ---
with col_center:
    if selected_crypto_name and selected_crypto_id:
        selected_crypto_info = realtime_df[realtime_df['id'] == selected_crypto_id].iloc[0] if realtime_df is not None and not realtime_df.empty else None
        
        if selected_crypto_info is not None:
            image = selected_crypto_info.get('image', 'https://www.coingecko.com/favicon.ico')
            symbol = selected_crypto_info.get('symbol', 'N/A').upper()
            st.markdown(
                f"## <img src='{image}' width='40'> {selected_crypto_name} ({symbol})",
                unsafe_allow_html=True
            )
        else:
             st.subheader(f"{selected_crypto_name}: Price Evolution")

        # Line 1: Evolution chart
        if not historical_df.empty:
            st.subheader("Historical Price Evolution")
            # --- Pass the selected period to the plotting function ---
            fig_price_evolution = plot_price_evolution_with_moving_averages(
                historical_df, 
                selected_crypto_id, 
                st.session_state.get('selected_time_period', 'All') # Use the stored period
            )
            st.plotly_chart(fig_price_evolution, use_container_width=True)
        else:
            st.warning(
                "No historical data available for analysis. "
                "Make sure to run `python src/fetch_and_save.py` "
                "and that JSON files are present in the `data/` folder."
            )
        
        st.markdown("---")

        # Line 2: Detailed Information/Insights (Styled Table) 
        st.subheader("Detailed Information")
        if selected_crypto_info is not None:
            details_df = pd.DataFrame({
                "Characteristic": [
                    "Current Price", "24h Change (%)", "Market Cap",
                    "24h Volume", "Lowest Price (24h)", "Highest Price (24h)"
                ],
                "Value": [
                    format_dataframe_value(selected_crypto_info.get('current_price'), prefix="$ ", decimals=4),
                    format_dataframe_value(selected_crypto_info.get('price_change_percentage_24h'), suffix="%", decimals=2),
                    format_dataframe_value(selected_crypto_info.get('market_cap'), prefix="$ ", decimals=0),
                    format_dataframe_value(selected_crypto_info.get('total_volume'), prefix="$ ", decimals=0),
                    format_dataframe_value(selected_crypto_info.get('low_24h'), prefix="$ ", decimals=4),
                    format_dataframe_value(selected_crypto_info.get('high_24h'), prefix="$ ", decimals=4)
                ]
            })
            st.dataframe(details_df.set_index("Characteristic"), use_container_width=True)
        else:
            st.info("Select a cryptocurrency to view detailed information.")
    else:
        st.info("Please select a cryptocurrency to display the analysis.")


# --- RIGHT COLUMN: Top 10 + Latest Daily Update ---
with col_right:
    st.subheader("Top 10 Cryptos 🏆")
    if realtime_df is not None and not realtime_df.empty:
        top_10_display_df = realtime_df.head(10).copy()
        
        top_10_display_df['Crypto'] = top_10_display_df.apply(
            lambda row: f"{row.get('name', 'N/A')} ({row.get('symbol', 'N/A').upper()})",
            axis=1
        )
        top_10_display_df['Current Price'] = top_10_display_df['current_price'].apply(lambda x: format_dataframe_value(x, prefix="$ ", decimals=2))
        top_10_display_df['24h Change (%)'] = top_10_display_df['price_change_percentage_24h']
        top_10_display_df['Market Cap'] = top_10_display_df['market_cap'].apply(lambda x: format_dataframe_value(x, prefix="$ ", decimals=0))
        top_10_display_df['Image URL'] = top_10_display_df['image'].apply(lambda x: x if isinstance(x, str) else "https://www.coingecko.com/favicon.ico")

        final_top_10_df = top_10_display_df[['Image URL', 'Crypto', 'Current Price', '24h Change (%)', 'Market Cap']]
        final_top_10_df.columns = ['Image', 'Crypto', 'Current Price', '24h Change (%)', 'Market Cap']

        st.markdown("##### Ranking by Market Cap")
        st.dataframe(
            final_top_10_df.style.map(
                lambda x: f"color: {'green' if x >= 0 else 'red'}",
                subset=['24h Change (%)']
            ).format(
                {'24h Change (%)': "{:.2f}%"},
                na_rep="N/A"
            ),
            hide_index=True,
            use_container_width=True,
            column_config={
                "Image": st.column_config.ImageColumn("Logo", width=40),
                "Crypto": st.column_config.Column("Name (Symbol)", width="medium"),
                "Current Price": st.column_config.Column(width="small"),
                "24h Change (%)": st.column_config.Column("24h Change (%)", width="small", help="Price change over the last 24 hours"),
                "Market Cap": st.column_config.Column(width="medium"),
            }
        )

    else:
        st.warning("Unable to load the Top 10 cryptos.")

    st.markdown("---")

    st.subheader("History 🗓️")
    data_dir = 'data'
    json_files = [f for f in os.listdir(data_dir) if f.startswith('crypto_data_') and f.endswith('.json')]
    if json_files:
        latest_file = sorted(json_files, reverse=True)[0]
        latest_date_str = latest_file.replace('crypto_data_', '').replace('.json', '')
        st.info(f"Latest saved historical data: **{latest_date_str}**")
        st.write("These data are used for evolution charts.")
    else:
        st.info("No historical saves found.")
        st.write("Run `python src/fetch_and_save.py` to start saving data.")