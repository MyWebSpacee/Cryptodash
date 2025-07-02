# Cryptodash
# CryptoDashboard 📈

---

## 🎯 Project Overview

**CryptoDashboard** is an interactive web application developed in **Python** that allows users to track major cryptocurrencies in real-time and analyze their historical evolution. Designed with a clean interface and interactive visualizations, this application is a simple and effective tool for anyone passionate or curious about the cryptocurrency market.

This project highlights skills in Python development (API, data processing, visualization), project organization, as well as automation and deployment of a web application.

---

## 🚀 Key Features

* **Real-Time Data:** Displays the Top 10 cryptocurrencies by market capitalization, including their current price, 24-hour change, volume, and market cap, updated regularly.
* **Automated Daily History:** A dedicated script retrieves and saves cryptocurrency data once a day in timestamped JSON files. This task is fully automated via a **GitHub Action**.
* **Interactive Visualizations:**
    * Price evolution chart over multiple days for a selected cryptocurrency.
    * Integration of moving averages (7 and 30 days) to identify trends.
    * Time filters (7 days, 1 month, 1 year, All) to analyze evolution over different periods.
* **User Interface:** Developed with **Streamlit**, the application offers easy navigation, responsive design, and clear presentation of information.
* **Key Indicators:** Displays important metrics (24h high/low price, volume, market cap) for the selected cryptocurrency.
* **Deployment:** The application is deployed on **Streamlit Cloud**, ensuring public accessibility and automatic updates.

---

## 💻 Technical Stack

* **Main Language:** Python 3.10+
* **Libraries:**
    * `requests`: For API calls.
    * `pandas`: For data manipulation and analysis.
    * `plotly`: For interactive graphical visualizations.
    * `streamlit`: For creating the web user interface.
* **External API:** CoinGecko (free API)
* **Automation:** GitHub Actions
* **Version Control:** Git + GitHub
* **Deployment:** Streamlit Cloud (free)
* **Data Format:** JSON (for historical data)
* **Recommended IDE:** VS Code

---

## 📂 Project Structure
cryptodashboard/
├── data/
│   └── (JSON files for historical data)
├── .github/
│   └── workflows/
│       └── save_data.yml        # GitHub Action for daily data saving
├── src/
│   ├── api/
│   │   └── coingecko.py         # Functions for interacting with the CoinGecko API
│   ├── utils/
│   │   └── data_processing.py   # (Can be extended for future data processing)
│   ├── visualizations/
│   │   └── plots.py             # Functions for creating Plotly charts
│   ├── app.py                   # Main Streamlit application
│   └── fetch_and_save.py        # Script for fetching and saving historical data
├── .gitignore                   # Files and folders to ignore by Git
├── requirements.txt             # List of Python dependencies
└── README.md                    # This documentation file

---

## 🛠️ Installation and Local Execution

Follow these steps to install and run CryptoDashboard on your machine.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/MyWebSpacee/Cryptodash.git
    cd Cryptodash
    ```

2.  **Create and Activate a Virtual Environment:**
    It is highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    # For Windows:
    .\venv\Scripts\activate
    # For macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Generate Initial Historical Data:**
    The dashboard requires historical data to display evolution charts. Run this script at least once (ideally multiple times on different days to see variations):
    ```bash
    python src/fetch_and_save.py
    ```
    *Note: Data will be automatically updated daily on the GitHub repository via GitHub Actions.*

5.  **Run the Streamlit Application:**
    Ensure you are in the root folder of `CryptoDashboard` in your terminal, then execute:
    ```bash
    streamlit run src/app.py
    ```
    The application will automatically open in your default web browser (usually at `http://localhost:8501`).

---

## ☁️ Deployment on Streamlit Cloud

This application is designed to be easily deployed on Streamlit Cloud.

1.  **GitHub Repository:** Ensure your project is pushed to a public GitHub repository.
2.  **Log in to Streamlit Cloud:** Go to [share.streamlit.io](https://share.streamlit.io/).
3.  **New Deployment:** Click "New app" and connect your GitHub repository.
    * **Repository:** Select `MyWebSpacee/Cryptodash`
    * **Branch:** `main` (or the branch you are using)
    * **Main file path:** [app.py](http://_vscodecontentref_/0)
4.  **Automatic Deployment:** To ensure your application updates with new data generated daily by GitHub Actions, make sure to enable the "Deploy on push" option in your app settings on Streamlit Cloud.

---

## 🖼️ Screenshots

---

### Dashboard Overview
![Overview of the CryptoDashboard showing key indicators, trend chart, and top 10.](assets/images/Cryptodash_overview.png)

---

### Price Evolution Chart
![Interactive chart showing the evolution of Bitcoin's price with moving averages and time filters.](assets/images/Price_Evolution.png)

---

### Top 10 Cryptocurrencies
![Table displaying the top 10 cryptocurrencies with their price, change, and market capitalization.](assets/images/Top_10_Table.png)

---

### Navigation
![List showing the choice of crypto to display.](assets/images/Navigation.png)

---

## 🧑‍💻 Developer

**Emmanuelle**  
[GitHub](https://github.com/MyWebSpacee)