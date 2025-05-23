# -*- coding: utf-8 -*-
"""kikoyi 00723.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zhlMaUQ0BR7vZDqbtdEgJ6K3-kLuu4A5
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings("ignore") #suppresses warnings for cleaner output
df=pd.read_csv('Kikoyis 00723.csv')
df.tail(10)

#combine year and mongth into a string
df['Date'] =df['Year'].astype(str) + '-' + df['Month'].astype(str)
#convert string into a datetime object
df['Date']=pd.to_datetime(df['Date'], format='mixed')
print(df)

#using bales sold as the time series
bales_sold = df['Bales Sold']
#plotting
plt.figure(figsize=(10,6))
plt.plot(df['Date'], bales_sold, marker='o', linestyle='-', color='b')
plt.title('Bales Sold Over Time')
plt.xlabel('Date')
plt.ylabel('Bales Sold')
plt.grid(True)

# stationarity check with adf  test
result=adfuller(bales_sold)
print('ADF Statistic:', result[0])
print('p value:', result[1])
print('Critical Values:', result[4])
if result[1] <= 0.05:
      print("The time series is stationary.")
else:
    print("The time series is not stationary.")

# Step 4: Fit SARIMA model
# Define SARIMA parameters: order=(p,d,q), seasonal_order=(P,D,Q,m)
# m=12 for monthly data with yearly seasonality
model = SARIMAX(bales_sold, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
sarima_model = model.fit()
print(sarima_model.summary())

#forecast for the next 12 months(2025)
forecast_steps =12
forecast = sarima_model.forecast(steps=forecast_steps)

#creating a data range for the dataset
last_date= df['Date'].iloc[-1]
forecast_dates= pd.date_range(start=last_date + pd.offsets.MonthBegin(1), periods=forecast_steps, freq='MS')
print("Forecast Dates:")
print(forecast_dates)
#creating a dataframe for the forecast
forecast_series= pd.Series(forecast.values, index=forecast_dates)
print("Forecasted Values:")
print(forecast_series)

#Visualizing the results
plt.figure(figsize=(10,6))
plt.plot(df['Date'], bales_sold, marker='o', linestyle='-', color='b', label='Historical Data')
plt.plot(forecast_series.index, forecast_series.values, marker='o', linestyle='--', color='r', label='Forecast')
plt.title('Bales Sold Forecast')
plt.xlabel('Date')
plt.ylabel('Bales Sold')
plt.legend()

!git init

!git add kikoyi 00723.ipynb

!cd /path/to/your/notebook/directory
!git add kikoyi 00723.ipynb