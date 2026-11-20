
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    ROOT / "data/processed/cleaned_sales.csv",
    parse_dates=["InvoiceDate"]
)

# Monthly revenue
monthly = (
    df.set_index("InvoiceDate")
    .resample("MS")["Revenue"]
    .sum()
    .asfreq("MS", fill_value=0)
)

data = monthly.to_frame("Revenue")

data["Month"] = data.index.month
data["Year"] = data.index.year

# Lag features
for lag in [1, 2, 3]:
    data[f"Lag_{lag}"] = data["Revenue"].shift(lag)

data = data.dropna()

features = [
    "Month", "Year",
    "Lag_1", "Lag_2", "Lag_3"
]

X = data[features]
y = data["Revenue"]

# Time-based split (no random shuffling)
split = int(len(data) * 0.8)
X_train = X.iloc[:split]
X_test = X.iloc[split:]
y_train = y.iloc[:split]
y_test = y.iloc[split:]

# Model
model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluation
predictions = model.predict(X_test)

print("MAE:", mean_absolute_error(
    y_test, predictions))

print("RMSE:", np.sqrt(
    mean_squared_error(y_test, predictions)))

# Forecast next three months recursively
history = monthly.copy()
future = []

for i in range(3):
    next_date = history.index[-1] + pd.offsets.MonthBegin(1)
    row = pd.DataFrame([{
        "Month": next_date.month,
        "Year": next_date.year,
        "Lag_1": history.iloc[-1],
        "Lag_2": history.iloc[-2],
        "Lag_3": history.iloc[-3]
    }])

    forecast = max(0,float(model.predict(row[features])[0]))
    future.append({
        "Month": next_date,
        "ForecastRevenue": forecast
    })

    history.loc[next_date] = forecast

forecast_df = pd.DataFrame(future)
forecast_df.to_csv(
    ROOT / "outputs/sales_forecast.csv",
    index=False)
print(forecast_df)
print("Forecast completed!")
