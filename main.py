import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Load historical data
data = pd.read_csv('AMZN.csv')  # Replace 'apple_stock_data.csv' with your file name

# Convert date to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Calculate moving averages
data['MA50'] = data['Close'].rolling(window=50).mean()
data['MA200'] = data['Close'].rolling(window=200).mean()

# Calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = calculate_rsi(data)

# Calculate MACD
def calculate_macd(data, short_window=12, long_window=26):
    short_ema = data['Close'].ewm(span=short_window, min_periods=1).mean()
    long_ema = data['Close'].ewm(span=long_window, min_periods=1).mean()
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=9, min_periods=1).mean()
    return macd, signal_line

data['MACD'], data['Signal_Line'] = calculate_macd(data)

# Calculate %K (Stochastic Oscillator)
def calculate_stochastic_oscillator(data, window=14):
    low_min = data['Low'].rolling(window=window).min()
    high_max = data['High'].rolling(window=window).max()
    stochastic_oscillator = ((data['Close'] - low_min) / (high_max - low_min)) * 100
    return stochastic_oscillator

data['%K'] = calculate_stochastic_oscillator(data)

# Simple Moving Average Crossover Strategy for buying and selling points
data['Signal'] = 0
data['Position'] = 0

data['Signal'][50:] = np.where(data['MA50'][50:] > data['MA200'][50:], 1, 0)
data['Position'] = data['Signal'].diff()

# Calculate profit and loss
initial_cash = 10000  # Initial investment amount
cash = initial_cash
shares = 0
buy_price = 0
sell_price = 0
transactions = []

for index, row in data.iterrows():
    if row['Position'] == 1:  # Buy signal
        if cash >= row['Close']:  # Check if enough cash to buy
            shares += cash // row['Close']  # Buy as many shares as possible with available cash
            cash -= shares * row['Close']  # Deduct spent cash
            buy_price = row['Close']
            transactions.append(('BUY', row['Date'], row['Close'], shares))
    elif row['Position'] == -1:  # Sell signal
        if shares > 0:  # Check if there are shares to sell
            cash += shares * row['Close']  # Add cash from selling shares
            sell_price = row['Close']
            transactions.append(('SELL', row['Date'], row['Close'], shares))
            shares = 0

# Calculate final value of investment
final_value = cash + (shares * data.iloc[-1]['Close'])
profit_loss = final_value - initial_cash

# Print profit/loss
print("Initial Investment: $", initial_cash)
print("Final Value: $", round(final_value, 2))
print("Profit/Loss: $", round(profit_loss, 2))

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Close'], label='Close Price')
plt.plot(data['Date'], data['MA50'], label='50-Day MA')
plt.plot(data['Date'], data['MA200'], label='200-Day MA')
plt.scatter(data[data['Position'] == 1]['Date'], data[data['Position'] == 1]['Close'], marker='^', color='g', label='Buy Signal')
plt.scatter(data[data['Position'] == -1]['Date'], data[data['Position'] == -1]['Close'], marker='v', color='r', label='Sell Signal')
plt.legend()
plt.title('Apple Stock Price with Moving Averages and Buy/Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

print("Transactions:")
for trans in transactions:
    print(trans)
