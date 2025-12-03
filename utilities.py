#Helper Functions

import matplotlib.pyplot as plt

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    stock_list.sort(key=lambda stock: stock.symbol)



# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key=lambda daily: daily.date)

# Function to create stock chart
def display_stock_chart(stock_list, symbol):
    # find the stock
    chosen = None
    for stock in stock_list:
        if stock.symbol.upper() == symbol.upper():
            chosen = stock
            break

    if chosen is None:
        print("Symbol not found.")
        return

    if not chosen.DataList:
        print("No data available to chart.")
        return

    # extract dates and closing prices
    dates = [daily.date for daily in chosen.DataList]
    closes = [daily.close for daily in chosen.DataList]

    # plot
    plt.figure(figsize=(10,5))
    plt.plot(dates, closes, marker='o')
    plt.title(f"{chosen.symbol} Closing Price History")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
