import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Example: If your data is multi-indexed by [date, SEHK_Code]:
# df = df.reset_index()

# --- 1. Prepare data for each SEHK Code ---
results = {}

for code in df['SEHK_Code'].unique():
    sub = df[df['SEHK_Code'] == code].sort_values('date').copy()
    
    # --- 2. Create the 1-lagged ATM volatility (target) ---
    sub['ATM_vol_target'] = sub['ATM_vol'].shift(-1)  # -1 for "future" ATM_vol as target, 1 for "past"
    
    # --- 3. Drop rows with NA from shifting ---
    sub = sub.dropna(subset=['ATM_vol', 'OInt', 'Volume', 'Call_OInt_Volume', 'Put_OInt_Volume', 'Volume_Total_OI', 'ATM_vol_target'])
    
    # --- 4. Features and target ---
    X = sub[['OInt', 'Volume', 'Call_OInt_Volume', 'Put_OInt_Volume', 'Volume_Total_OI']]
    y = sub['ATM_vol_target']
    
    # --- 5. Train/test split (optional, here 80/20) ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)
    
    # --- 6. Ridge regression ---
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train, y_train)
    
    # --- 7. Predict and evaluate ---
    y_pred = ridge.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    # --- 8. Store results ---
    results[code] = {
        'model': ridge,
        'mse': mse,
        'coef': ridge.coef_,
        'intercept': ridge.intercept_,
        'feature_names': X.columns.tolist()
    }
    print(f"SEHK Code: {code}, Test MSE: {mse:.4f}")

# --- 9. Example: Access coefficients for a code ---
for code, res in results.items():
    print(f"\nSEHK Code: {code}")
    for fname, coef in zip(res['feature_names'], res['coef']):
        print(f"  {fname}: {coef:.5f}")
