# Quanto forward hedging for energy market https://research-api.cbs.dk/ws/portalfiles/portal/45713609/nina_lange_pricing_and_hedging_quanto_options_publishersversion.pdf

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Step 1: Load or generate historical data
# Replace this synthetic data with your actual TAIEX and USD/TWD time series data
np.random.seed(42)  # For reproducibility
dates = pd.date_range(start='2020-01-01', end='2025-07-21', freq='B')  # Business days
taiex = pd.Series(10000 + np.cumsum(np.random.normal(0, 50, len(dates))), index=dates)  # Synthetic TAIEX data
usd_twd = pd.Series(30 + np.cumsum(np.random.normal(0, 0.1, len(dates))), index=dates)  # Synthetic USD/TWD data

# Step 2: Calculate correlation between TAIEX and USD/TWD
correlation = taiex.corr(usd_twd)
print(f"Correlation between TAIEX and USD/TWD: {correlation:.4f}")
print("Note: A negative correlation indicates TAIEX rises as TWD strengthens (USD/TWD falls).")

# Step 3: Define simulation functions
def simulate_quanto_forward(taiex, strike_price, fixed_fx_rate):
    """
    Simulate the payoff of a quanto forward contract.
    Parameters:
        taiex: pandas Series of TAIEX prices
        strike_price: Forward strike price (e.g., initial TAIEX level)
        fixed_fx_rate: Fixed FX rate for converting TWD payoff to USD
    Returns:
        Payoff in USD: (S_T - K) * fixed_fx_rate
    """
    S_T = taiex.iloc[-1]  # TAIEX at maturity
    payoff = (S_T - strike_price) * fixed_fx_rate
    return payoff

def simulate_taiex_futures_unhedged(taiex, strike_price, usd_twd):
    """
    Simulate the payoff of TAIEX futures converted to USD at spot rate (unhedged FX).
    Parameters:
        taiex: pandas Series of TAIEX prices
        strike_price: Forward strike price
        usd_twd: pandas Series of USD/TWD exchange rates
    Returns:
        Payoff in USD: (S_T - K) / usd_twd_T
    """
    S_T = taiex.iloc[-1]  # TAIEX at maturity
    fx_T = usd_twd.iloc[-1]  # Spot FX rate at maturity
    payoff_twd = S_T - strike_price
    payoff_usd = payoff_twd / fx_T
    return payoff_usd

# Step 4: Define trade parameters
strike_price = 10000  # Strike price (e.g., initial TAIEX level)
fixed_fx_rate = 30  # Fixed FX rate for quanto forward (e.g., 30 TWD/USD)

# Step 5: Simulate trades
quanto_pay imported = simulate_quanto_forward(taiex, strike_price, fixed_fx_rate)
unhedged_payoff = simulate_taiex_futures_unhedged(taiex, strike_price, usd_twd)

# Step 6: Display results
print(f"\nSimulation Results:")
print(f"Quanto forward payoff: {quanto_payoff:.2f} USD")
print(f"Unhedged TAIEX futures payoff: {unhedged_payoff:.2f} USD")
print(f"Difference (Quanto - Unhedged): {quanto_payoff - unhedged_payoff:.2f} USD")
print("Note: A positive difference suggests the quanto forward outperforms the unhedged strategy.")
