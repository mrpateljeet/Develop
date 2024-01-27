import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Download historical data
ticker = 'AAPL'
start_date = '2020-01-01'
end_date = '2023-01-01'
data = yf.download(ticker, start=start_date, end=end_date)

# Calculate Simple Moving Averages (SMA)
data['SMA50'] = data['Close'].rolling(window=50).mean()
data['SMA200'] = data['Close'].rolling(window=200).mean()

# Calculate Exponential Moving Averages (EMA)
data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean()

# Define trading signals based on crossovers
data['SMA_Signal'] = 0
data['SMA_Signal'][50:] = np.where(data['SMA50'][50:] > data['SMA200'][50:], 1, -1)

data['EMA_Signal'] = 0
data['EMA_Signal'][50:] = np.where(data['EMA50'][50:] > data['EMA200'][50:], 1, -1)

# Backtesting (calculate returns)
data['Daily_Return'] = data['Close'].pct_change()

# SMA strategy
data['SMA_Strategy_Return'] = data['SMA_Signal'].shift(1) * data['Daily_Return']

# EMA strategy
data['EMA_Strategy_Return'] = data['EMA_Signal'].shift(1) * data['Daily_Return']

# Export data to CSV
csv_filename = 'trading_strategy_results.csv'
data.to_csv(csv_filename, index=True)

# Visualize
plt.figure(figsize=(12, 8))
plt.plot(data['Close'], label='Close Price', alpha=0.5)
plt.plot(data['SMA50'], label='SMA50')
plt.plot(data['SMA200'], label='SMA200')
plt.plot(data[data['SMA_Signal'] == 1].index, data['SMA50'][data['SMA_Signal'] == 1], '^', markersize=10, color='g', label='SMA Buy Signal')
plt.plot(data[data['SMA_Signal'] == -1].index, data['SMA50'][data['SMA_Signal'] == -1], 'v', markersize=10, color='r', label='SMA Sell Signal')

plt.plot(data['EMA50'], label='EMA50')
plt.plot(data['EMA200'], label='EMA200')
plt.plot(data[data['EMA_Signal'] == 1].index, data['EMA50'][data['EMA_Signal'] == 1], '^', markersize=10, color='b', label='EMA Buy Signal')
plt.plot(data[data['EMA_Signal'] == -1].index, data['EMA50'][data['EMA_Signal'] == -1], 'v', markersize=10, color='y', label='EMA Sell Signal')

plt.title(f'{ticker} Double Moving Averages Crossover System')
plt.legend()
plt.show()
