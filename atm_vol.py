# https://quant.stackexchange.com/questions/32725/dynamic-hedge-of-quanto-options

import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import datetime, timedelta

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# --- Generate Synthetic ATM Volatility Data ---
np.random.seed(42)  # For reproducibility
trading_days = 126  # 6 months * 21 trading days/month
tickers = ['700.HK', '9988.HK', '1211.HK']
dates = [datetime(2025, 1, 21) + timedelta(days=i) for i in range(trading_days)]
obs_per_day = 3

# Create synthetic ATM volatility data (3 observations per day)
data = []
for ticker in tickers:
    for date in dates:
        for obs in range(obs_per_day):
            # Simulate ATM volatility (20-40% range, with ticker-specific variation)
            base_vol = 30 if ticker == '700.HK' else 25 if ticker == '9988.HK' else 35  # Tencent, Alibaba, BYD
            vol = base_vol + np.random.normal(0, 5)  # Add noise
            vol = max(20, min(40, vol))  # Bound between 20% and 40%
            data.append({
                'Ticker': ticker,
                'Date': date,
                'ATM_Vol': round(vol, 2)
            })

vol_df = pd.DataFrame(data)

# Aggregate to daily ATM volatility (mean of 3 observations per day)
daily_vol_df = vol_df.groupby(['Ticker', 'Date'])['ATM_Vol'].mean().reset_index()
daily_vol_df['ATM_Vol'] = daily_vol_df['ATM_Vol'].round(2)

# Compute summary statistics for the table
stats_df = daily_vol_df.groupby('Ticker')['ATM_Vol'].agg(
    Mean='mean',
    Median='median',
    Min='min',
    Max='max',
    Std='std'
).reset_index()
stats_df = stats_df.round(2)

# Create box plots
fig = px.box(
    daily_vol_df,
    x='Ticker',
    y='ATM_Vol',
    title='Daily ATM Volatility (95–105% Moneyness) Over Last 6 Months',
    labels={'ATM_Vol': 'ATM Volatility (%)', 'Ticker': 'Ticker'},
    template='plotly_white'
)
fig.update_layout(
    xaxis_title='Ticker',
    yaxis_title='ATM Volatility (%)',
    showlegend=False,
    height=500
)

# --- Existing Data for Page 1 (Market Overview) ---
try:
    market_df = pd.read_csv('trading_data.csv')
except FileNotFoundError:
    market_df = pd.DataFrame({
        'Ticker': ['700.HK', '9988.HK', '1211.HK'],
        'Underlying_Name': ['Tencent Holdings', 'Alibaba Group', 'BYD Company'],
        'OInt_Calls': [1000, 1500, 2000],
        'OInt_Puts': [800, 1200, 1800],
        'Volume': [500, 700, 1000],
        'Spot': [350.25, 80.50, 220.75],
        'Contract_Size': [100, 100, 100],
        'IV': [30.5, 25.3, 35.7]
    })

# Compute derived columns for Page 1
market_df['Total_OInt'] = market_df['OInt_Calls'] + market_df['OInt_Puts']
market_df['Put_Call_Ratio'] = market_df.apply(
    lambda x: x['OInt_Puts'] / x['OInt_Calls'] if x['OInt_Calls'] != 0 else float('inf'), axis=1
)
market_df['Total_Notional_Traded'] = market_df['Volume'] * market_df['Spot'] * market_df
