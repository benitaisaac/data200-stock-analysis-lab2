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
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Return to Manage Stocks")
        option = input("Enter Menu Option: ")

        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)
        elif option == "0":
            print("Returning to Manage Stocks...")
            input("Press Enter to continue...")
        else:
            print("*** Invalid Option - Try again ***")
            input("Press Enter to continue...")



# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---\n")

    if not stock_list:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    print("Stocks Being Tracked:")
    for stock in stock_list:
        print(f"- {stock.symbol} ({stock.name})")

    symbol = input("\nEnter stock symbol to buy: ").upper()
    amount_text = input("Enter number of shares to buy: ")

    try:
        amount = float(amount_text)
    except ValueError:
        print("Invalid number of shares.")
        input("Press Enter to continue...")
        return

    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            stock.buy(amount)
            print(f"\nUpdated {symbol}: now has {stock.shares} shares.")
            found = True
            break

    if not found:
        print("\nStock symbol not found.")

    input("Press Enter to continue...")


# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---\n")

    if not stock_list:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    print("Stocks Being Tracked:")
    for stock in stock_list:
        print(f"- {stock.symbol} ({stock.name})")

    symbol = input("\nEnter stock symbol to sell: ").upper()
    amount_text = input("Enter number of shares to sell: ")

    try:
        amount = float(amount_text)
    except ValueError:
        print("Invalid number of shares.")
        input("Press Enter to continue...")
        return

    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            try:
                stock.sell(amount)
                print(f"\nUpdated {symbol}: now has {stock.shares} shares.")
            except Exception as e:
                # In case your Stock.sell() has any checks
                print("\nError while selling shares:", e)
            found = True
            break

    if not found:
        print("\nStock symbol not found.")

    input("Press Enter to continue...")


# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---\n")

    if not stock_list:
        print("No stocks in portfolio.")
        input("Press Enter to continue...")
        return

    print("Stocks Being Tracked:")
    for stock in stock_list:
        print(f"- {stock.symbol} ({stock.name})")

    symbol = input("\nEnter stock symbol to delete: ").upper()

    index_to_remove = -1
    for i, stock in enumerate(stock_list):
        if stock.symbol == symbol:
            index_to_remove = i
            break

    if index_to_remove == -1:
        print("\nStock symbol not found.")
    else:
        confirm = input(f"Are you sure you want to delete {symbol}? (y/n): ").lower()
        if confirm == "y":
            removed = stock_list.pop(index_to_remove)
            print(f"\n{removed.symbol} removed from portfolio.")
        else:
            print("\nDelete cancelled.")

    input("Press Enter to continue...")



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
    print("Add Daily Stock Data ---\n")

    if not stock_list:
        print("No stocks in portfolio. Add stocks first.")
        input("Press Enter to continue...")
        return

    print("Stocks Being Tracked:")
    for stock in stock_list:
        print(f"- {stock.symbol} ({stock.name})")

    symbol = input("\nEnter stock symbol to add data for: ").upper()

    chosen_stock = None
    for stock in stock_list:
        if stock.symbol == symbol:
            chosen_stock = stock
            break

    if chosen_stock is None:
        print("\nStock symbol not found.")
        input("Press Enter to continue...")
        return

    date_str = input("Enter date (m/d/yy): ")
    price_str = input("Enter closing price: ")
    volume_str = input("Enter volume: ")

    try:
        date = datetime.strptime(date_str, "%m/%d/%y")
        price = float(price_str)
        volume = int(volume_str)
    except ValueError:
        print("\nInvalid date, price, or volume.")
        input("Press Enter to continue...")
        return

    # Create a DailyData object and add it to this stock
    daily = DailyData(date, price, volume)
    chosen_stock.DataList.append(daily)

    print("\nDaily data added successfully.")
    input("Press Enter to continue...")


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