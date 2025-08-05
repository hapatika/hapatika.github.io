import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV, train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Cross validation grid search alpha
# -------------- Configuration --------------
# Your DataFrame: df (as described above)
# If needed, ensure date is sorted and not duplicated
df = df.sort_values(['SEHK_Code', 'date'])  # Replace with your sorting
alphas = np.logspace(-3, 2, 10)  # Grid for Ridge regularization

results = {}

for code in df['SEHK_Code'].unique():
    sub = df[df['SEHK_Code'] == code].copy()
    sub = sub.sort_values('date')
    sub['ATM_vol_target'] = sub['ATM_vol'].shift(-1)
    sub = sub.dropna(subset=['ATM_vol_target', 'OInt', 'Volume', 'Call_OInt_Volume', 'Put_OInt_Volume', 'Volume_Total_OI'])

    X = sub[['OInt', 'Volume', 'Call_OInt_Volume', 'Put_OInt_Volume', 'Volume_Total_OI']].values
    y = sub['ATM_vol_target'].values

    # --- Time series split for CV ---
    tscv = TimeSeriesSplit(n_splits=5)
    ridge = Ridge()
    grid = GridSearchCV(ridge, param_grid={'alpha': alphas}, cv=tscv, scoring='neg_mean_squared_error')
    grid.fit(X, y)
    best_alpha = grid.best_params_['alpha']
    print(f"SEHK {code}: best alpha={best_alpha:.4f}, best CV MSE={-grid.best_score_:.4f}")

    # --- Out-of-sample test split (last 20% as test) ---
    n = len(y)
    n_train = int(n * 0.8)
    X_train, X_test = X[:n_train], X[n_train:]
    y_train, y_test = y[:n_train], y[n_train:]

    ridge_best = Ridge(alpha=best_alpha)
    ridge_best.fit(X_train, y_train)
    y_pred = ridge_best.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    # --- Store results ---
    results[code] = {
        'model': ridge_best,
        'y_test': y_test,
        'y_pred': y_pred,
        'test_idx': sub.index[n_train:],
        'mse': mse,
        'coef': ridge_best.coef_,
        'intercept': ridge_best.intercept_,
        'feature_names': sub[['OInt', 'Volume', 'Call_OInt_Volume', 'Put_OInt_Volume', 'Volume_Total_OI']].columns.tolist(),
        'best_alpha': best_alpha
    }

    # --- Out-of-sample prediction plot ---
    plt.figure(figsize=(7, 4))
    plt.plot(sub['date'].iloc[n_train:], y_test, label='True')
    plt.plot(sub['date'].iloc[n_train:], y_pred, label='Predicted', linestyle='--')
    plt.title(f'ATM Volatility Prediction (SEHK {code})')
    plt.xlabel('Date')
    plt.ylabel('ATM Volatility (1-day ahead)')
    plt.legend()
    plt.tight_layout()
    plt.show()

# One model
# --- Prepare one big DataFrame with all codes ---
df2 = df.copy()
df2 = df2.sort_values(['SEHK_Code', 'date'])
df2['ATM_vol_target'] = df2.groupby('SEHK_Code')['ATM_vol'].shift(-1)
df2 = df2.dropna(subset=['ATM_vol_target', 'OInt', 'Volume', 'Call_OInt_Volume', 'Put_OInt_Volume', 'Volume_Total_OI'])

X_all = df2[['OInt', 'Volume', 'Call_OInt_Volume', 'Put_OInt_Volume', 'Volume_Total_OI']]
y_all = df2['ATM_vol_target']

# Optional: add dummy variables for SEHK_Code if you want to account for code effect
# X_all = pd.get_dummies(X_all.join(df2['SEHK_Code']), columns=['SEHK_Code'])

# --- Split last 20% as out-of-sample test ---
n = len(y_all)
n_train = int(n * 0.8)
X_train_all, X_test_all = X_all.iloc[:n_train], X_all.iloc[n_train:]
y_train_all, y_test_all = y_all.iloc[:n_train], y_all.iloc[n_train:]

# --- Grid search cross-validation for alpha (using TimeSeriesSplit) ---
tscv = TimeSeriesSplit(n_splits=5)
ridge = Ridge()
grid = GridSearchCV(ridge, param_grid={'alpha': alphas}, cv=tscv, scoring='neg_mean_squared_error')
grid.fit(X_train_all, y_train_all)
best_alpha_all = grid.best_params_['alpha']
print(f"\n[ALL TICKERS] Best alpha: {best_alpha_all:.4f}, best CV MSE: {-grid.best_score_:.4f}")

# --- Final model on all training data ---
ridge_all = Ridge(alpha=best_alpha_all)
ridge_all.fit(X_train_all, y_train_all)
y_pred_all = ridge_all.predict(X_test_all)
mse_all = mean_squared_error(y_test_all, y_pred_all)
print(f"[ALL TICKERS] Test MSE: {mse_all:.4f}")

# --- Plot out-of-sample predictions (all tickers) ---
plt.figure(figsize=(10, 4))
plt.plot(df2['date'].iloc[n_train:], y_test_all, label='True')
plt.plot(df2['date'].iloc[n_train:], y_pred_all, label='Predicted', linestyle='--')
plt.title('ATM Volatility Prediction (All Tickers, Out-of-sample)')
plt.xlabel('Date')
plt.ylabel('ATM Volatility (1-day ahead)')
plt.legend()
plt.tight_layout()
plt.show()
