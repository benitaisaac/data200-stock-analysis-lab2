from os import system, name
import matplotlib.pyplot as plt


# Function to Clear the Screen
def clear_screen():
    if name == "nt":  # User is running Windows
        _ = system("cls")
    else:  # User is running Linux or Mac
        _ = system("clear")


# Function to sort the stock list (alphabetical by symbol)
def sortStocks(stock_list):
    """
    Simple bubble sort for stock_list using stock.symbol.
    Avoids lambda or advanced features.
    """
    n = len(stock_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if stock_list[j].symbol > stock_list[j + 1].symbol:
                temp = stock_list[j]
                stock_list[j] = stock_list[j + 1]
                stock_list[j + 1] = temp


# Function to sort each stock's daily data by date (oldest first)
def sortDailyData(stock_list):
    """
    Bubble sort for each stock's DataList using daily.date.
    """
    for stock in stock_list:
        n = len(stock.DataList)
        for i in range(n):
            for j in range(0, n - i - 1):
                if stock.DataList[j].date > stock.DataList[j + 1].date:
                    temp = stock.DataList[j]
                    stock.DataList[j] = stock.DataList[j + 1]
                    stock.DataList[j + 1] = temp


# Function to create stock price chart
def display_stock_chart(stock_list, symbol):
    """
    Finds stock by symbol and plots its closing prices using matplotlib.
    Written using only basic loops (no list comprehensions).
    """
    # find the stock object
    chosen_stock = None
    for stock in stock_list:
        if stock.symbol.upper() == symbol.upper():
            chosen_stock = stock
            break

    if chosen_stock is None:
        print("Symbol not found.")
        return

    # sort daily data by date (in case it's not sorted yet)
    sortDailyData(stock_list)

    if len(chosen_stock.DataList) == 0:
        print("No data available to chart.")
        return

    # Build dates list the simple way
    dates = []
    closes = []
    for daily in chosen_stock.DataList:
        dates.append(daily.date)
        closes.append(daily.close)

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(dates, closes, marker="o")
    plt.title(chosen_stock.symbol + " Closing Price History")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
