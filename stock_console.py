# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    clear_screen()
    print("Add Stock ---")
    symbol = input("Enter stock symbol: ").upper()
    name = input("Enter stock name: ")
    shares = float(input("Enter number of shares: "))
    new_stock = Stock(symbol, name, shares)
    stock_list.append(new_stock)
    print("Stock added!")
    input("Press Enter to continue...")

        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        pass


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print("Stock List: [",end="")
    pass

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    pass

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    pass


# List stocks being tracked
# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("Stocks Being Tracked ---\n")
    if not stock_list:
        print("No stocks in portfolio.")
    else:
        for stock in stock_list:
            print(f"{stock.symbol} - {stock.name} - {stock.shares} shares")
    print()
    input("Press Enter to continue...")


# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    pass

# Display Report for All Stocks
def display_report(stock_list):
    clear_screen()
    print("Stock Report ---\n")

    if not stock_list:
        print("No stocks in portfolio.")
        input("\nPress Enter to continue...")
        return

    for stock in stock_list:
        # Basic info
        line = f"{stock.symbol} - {stock.name} - {stock.shares} shares"

        # Try to show latest price & value if we have history
        last_price = None
        if hasattr(stock, "DataList") and stock.DataList:
            # assume DataList is in date order, take last
            last_price = stock.DataList[-1].close

        if last_price is not None:
            value = stock.shares * last_price
            line += f" | Last Price: ${last_price:0.2f} | Value: ${value:0.2f}"

        print(line)

    input("\nPress Enter to continue...")



  


# Display Chart
def display_chart(stock_list):
    clear_screen()
    print("Display Stock Chart ---\n")

    if not stock_list:
        print("No stocks in portfolio.")
        input("\nPress Enter to continue...")
        return

    # Show available symbols
    print("Available Stocks:")
    for stock in stock_list:
        print(f"- {stock.symbol}")

    symbol = input("\nEnter stock symbol to chart: ").upper()

    # Call helper from utilities.py
    try:
        display_stock_chart(stock_list, symbol)
    except Exception as e:
        print("\nError displaying chart:", e)
        input("\nPress Enter to continue...")


# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Data to Database")
        print("2 - Load Data from Database")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")

        while option not in ["1", "2", "3", "4", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Manage Data ---")
            print("1 - Save Data to Database")
            print("2 - Load Data from Database")
            print("3 - Retrieve Data from Web")
            print("4 - Import from CSV File")
            print("0 - Exit Manage Data")
            option = input("Enter Menu Option: ")

        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("Data saved to database.")
            input("Press Enter to continue...")
        elif option == "2":
            stock_data.load_stock_data(stock_list)
            print("Data loaded from database.")
            input("Press Enter to continue...")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)  # will implement this later in section 2 of the lab
        else:
            print("Returning to Main Menu...")
            input("Press Enter to continue...")



# Get stock price and volume history from Yahoo! Finance using Web Scraping
# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieve Data from Web ---")

    if len(stock_list) == 0:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    dateStart = input("Enter starting date (m/d/yy): ")
    dateEnd = input("Enter ending date (m/d/yy): ")

    try:
        recordCount = stock_data.retrieve_stock_web(dateStart, dateEnd, stock_list)
        print(f"{recordCount} records retrieved.")
    except RuntimeWarning as e:
        print("Error:", e)
        print("Check your ChromeDriver installation / PATH.")
    except Exception as e:
        print("An unexpected error occurred while retrieving data:", e)

    input("Press Enter to continue...")


# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import Data from CSV File ---\n")

    if len(stock_list) == 0:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    symbol = input("Enter stock symbol to import data for: ").upper()
    filename = input("Enter full path to CSV file: ")

    try:
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
        print(f"\nImport complete for {symbol}.")
    except FileNotFoundError:
        print("\nFile not found. Check the path and try again.")
    except Exception as e:
        print("\nAn error occurred while importing data:", e)

    input("\nPress Enter to continue...")


# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()