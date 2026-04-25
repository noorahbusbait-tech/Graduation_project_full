# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split, TimeSeriesSplit, GridSearchCV

# 1. Create directory for results
if not os.path.exists('outputs'):
    os.makedirs('outputs')

# 2. Load Data
df = pd.read_csv('cleandata.csv')

# 3. Data Prep
df['Adm_Date'] = pd.to_datetime(df['Adm. Date/Time']).dt.date
daily_los = df.groupby('Adm_Date')['LOS'].mean().reset_index()

min_date = daily_los['Adm_Date'].min()
max_date = daily_los['Adm_Date'].max()
date_range = pd.date_range(start=min_date, end=max_date, freq='D')

# Updated fillna to modern pandas syntax
daily_los = daily_los.set_index('Adm_Date').reindex(date_range).ffill().reset_index()
daily_los = daily_los.rename(columns={'index': 'Adm_Date'})

# --- Time Series Prep ---
def create_lagged_features(df, column, num_lags):
    for i in range(1, num_lags + 1):
        df[f'{column}_lag_{i}'] = df[column].shift(i)
    return df

num_lags = 7
daily_los_features = create_lagged_features(daily_los.copy(), 'LOS', num_lags)
daily_los_features.dropna(inplace=True)

X = daily_los_features[[f'LOS_lag_{i}' for i in range(1, num_lags + 1)]]
y = daily_los_features['LOS']

forecast_horizon = 21
X_train = X.iloc[:-forecast_horizon]
y_train = y.iloc[:-forecast_horizon]

model_ts = RandomForestRegressor(n_estimators=100, random_state=42)
model_ts.fit(X_train, y_train)

# --- Forecasting ---
last_known_data = daily_los['LOS'].tail(num_lags).tolist()
future_predictions = []
future_dates = pd.date_range(start=daily_los['Adm_Date'].max() + pd.Timedelta(days=1), periods=forecast_horizon, freq='D')

for _ in range(forecast_horizon):
    input_features = np.array(last_known_data[-num_lags:]).reshape(1, -1)
    next_pred = model_ts.predict(input_features)[0]
    future_predictions.append(next_pred)
    last_known_data.append(next_pred)

future_forecast_df = pd.DataFrame({'Adm_Date': future_dates, 'Forecasted_LOS': future_predictions})

# --- True Census Logic ---
temp_df = df.copy()
temp_df['Entry'] = pd.to_datetime(temp_df['Adm. Date/Time'])
temp_df['Exit'] = pd.to_datetime(temp_df['DSC Time Clean'])
mask = temp_df['Exit'].isna()
temp_df.loc[mask, 'Exit'] = temp_df.loc[mask, 'Entry'] + pd.to_timedelta(temp_df.loc[mask, 'LOS'], unit='D')

all_dates = pd.date_range(start=temp_df['Entry'].min().date(), end=temp_df['Entry'].max().date())
census_data = [{'Date': d, 'True_Occupancy': ((temp_df['Entry'].dt.date <= d.date()) & (temp_df['Exit'].dt.date > d.date())).sum()} for d in all_dates]
daily_census_df = pd.DataFrame(census_data)

# --- Final XGBoost Model ---
num_lags_census = 7
for i in range(1, num_lags_census + 1):
    daily_census_df[f'census_lag_{i}'] = daily_census_df['True_Occupancy'].shift(i)
daily_census_df.dropna(inplace=True)

X_census = daily_census_df[[f'census_lag_{i}' for i in range(1, num_lags_census + 1)]]
y_census = daily_census_df['True_Occupancy']

# Tuned Hyperparameters from your previous run
best_params = {'learning_rate': 0.05, 'max_depth': 5, 'n_estimators': 100, 'subsample': 0.8}
final_xgb_model = xgb.XGBRegressor(**best_params, random_state=42)
final_xgb_model.fit(X_census, y_census)

# Generate Final 7-Day Forecast
last_vals = y_census.tail(num_lags_census).tolist()
final_forecast = []
for _ in range(7):
    inp_arr = np.array(last_vals[-num_lags_census:]).reshape(1, -1)
    p = final_xgb_model.predict(inp_arr)[0]
    p = min(80, max(0, p))
    final_forecast.append(p)
    last_vals.append(p)

final_forecast_dates = pd.date_range(start=daily_census_df['Date'].max() + pd.Timedelta(days=1), periods=7)
final_tuned_df = pd.DataFrame({'Date': final_forecast_dates.astype(str), 'Tuned_Predicted_Occupancy': final_forecast})

# --- Save Outputs ---
print("Final Forecast Results:")
print(final_tuned_df)

# Calculate Shortage Risk
capacity = 80
over_capacity_days = sum(1 for p in final_forecast if p > capacity)
# Risk level based on number of days over capacity
if over_capacity_days == 0:
    risk_text = "Low - No overcapacity predicted."
elif over_capacity_days <= 2:
    risk_text = f"Moderate - {over_capacity_days} days near limit."
else:
    risk_text = f"High - {over_capacity_days} days over capacity!"

# Save JSON with both the table data and the risk summary
output_data = {
    "forecast": final_tuned_df.to_dict(orient="records"),
    "shortage_risk": risk_text
}

import json
with open("finaloccupancy.json", "w") as f:
    json.dump(output_data, f)

with open("outputs/finaloccupancy.json", "w") as f:
    json.dump(output_data, f)


# Generate and Save Charts
# 1. Demand Chart
plt.figure(figsize=(10, 5))
plt.plot(future_forecast_df['Adm_Date'], future_forecast_df['Forecasted_LOS'], color='green', marker='o')
plt.title('Daily Average LOS Forecast')
plt.savefig("outputs/demandchart.png")
plt.close()

# 2. Occupancy Chart
plt.figure(figsize=(10, 5))
plt.plot(final_tuned_df['Date'], final_tuned_df['Tuned_Predicted_Occupancy'], color='darkgreen', marker='o')
plt.axhline(y=80, color='red', linestyle='--', label='80 Bed Capacity')
plt.title('7-Day Bed Occupancy Forecast')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/occupancychart.png")
plt.close()

print("All charts and data saved to outputs/ and root.")
