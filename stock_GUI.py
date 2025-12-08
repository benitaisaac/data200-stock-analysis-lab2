# Summary: This module contains the user interface and logic for a graphical user interface version
# of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData


class StockApp:
    def __init__(self):
        self.stock_list = []
        # check for database, create if not exists
        if path.exists("stocks.db") is False:
            stock_data.create_database()

        # ----- Window -----
        self.root = Tk()
        self.root.title("Benita's Stock Manager")

        # ----- Menubar -----
        self.menubar = Menu(self.root)

        # File Menu
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Load Data", command=self.load)
        filemenu.add_command(label="Save Data", command=self.save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        # Web Menu
        webmenu = Menu(self.menubar, tearoff=0)
        webmenu.add_command(
            label="Scrape Data from Yahoo! Finance...",
            command=self.scrape_web_data,
        )
        webmenu.add_command(
            label="Import CSV from Yahoo! Finance...",
            command=self.importCSV_web_data,
        )
        self.menubar.add_cascade(label="Web", menu=webmenu)

        # Chart Menu
        chartmenu = Menu(self.menubar, tearoff=0)
        chartmenu.add_command(
            label="Display Price Chart",
            command=self.display_chart,
        )
        self.menubar.add_cascade(label="Chart", menu=chartmenu)

        self.root.config(menu=self.menubar)

        # ----- Heading -----
        heading_frame = ttk.Frame(self.root)
        heading_frame.pack(fill="x", padx=10, pady=10)

        self.headingLabel = ttk.Label(
            heading_frame,
            text="No stock selected",
            font=("Helvetica", 14, "bold"),
        )
        self.headingLabel.pack(side="left")

        # ----- Main layout (list + tabs) -----
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left: stock list
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="y")

        ttk.Label(left_frame, text="Stocks").pack(anchor="w")
        self.stockList = Listbox(left_frame, width=20, height=15)
        self.stockList.pack(side="left", fill="y")

        stock_scroll = ttk.Scrollbar(
            left_frame, orient="vertical", command=self.stockList.yview
        )
        stock_scroll.pack(side="right", fill="y")
        self.stockList.config(yscrollcommand=stock_scroll.set)

        # When selection changes, update history/report
        self.stockList.bind("<<ListboxSelect>>", self.update_data)

        # Right: tabs
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

        self.tabs = ttk.Notebook(right_frame)
        self.tabs.pack(fill="both", expand=True)

        self.main_tab = ttk.Frame(self.tabs)
        self.history_tab = ttk.Frame(self.tabs)
        self.report_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.main_tab, text="Main")
        self.tabs.add(self.history_tab, text="History")
        self.tabs.add(self.report_tab, text="Report")

        # ----- Main Tab: Add / Update / Delete -----
        add_frame = ttk.LabelFrame(self.main_tab, text="Add Stock")
        add_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(add_frame, text="Symbol:").grid(row=0, column=0, sticky="e")
        self.addSymbolEntry = ttk.Entry(add_frame, width=10)
        self.addSymbolEntry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(add_frame, text="Name:").grid(row=1, column=0, sticky="e")
        self.addNameEntry = ttk.Entry(add_frame, width=25)
        self.addNameEntry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(add_frame, text="Shares:").grid(row=2, column=0, sticky="e")
        self.addSharesEntry = ttk.Entry(add_frame, width=10)
        self.addSharesEntry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Button(add_frame, text="Add Stock", command=self.add_stock).grid(
            row=3, column=0, columnspan=2, pady=5
        )

        # Update shares section
        update_frame = ttk.LabelFrame(self.main_tab, text="Update Shares")
        update_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(update_frame, text="Shares (+/-):").grid(row=0, column=0, sticky="e")
        self.updateSharesEntry = ttk.Entry(update_frame, width=10)
        self.updateSharesEntry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Button(update_frame, text="Buy", command=self.buy_shares).grid(
            row=1, column=0, padx=5, pady=5
        )
        ttk.Button(update_frame, text="Sell", command=self.sell_shares).grid(
            row=1, column=1, padx=5, pady=5
        )

        # Delete stock
        delete_frame = ttk.Frame(self.main_tab)
        delete_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(
            delete_frame,
            text="Delete Selected Stock",
            command=self.delete_stock,
        ).pack(anchor="w")

        # ----- History Tab -----
        history_frame = ttk.Frame(self.history_tab)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.dailyDataList = Text(history_frame, width=60, height=15)
        self.dailyDataList.pack(side="left", fill="both", expand=True)

        history_scroll = ttk.Scrollbar(
            history_frame, orient="vertical", command=self.dailyDataList.yview
        )
        history_scroll.pack(side="right", fill="y")
        self.dailyDataList.config(yscrollcommand=history_scroll.set)

        # ----- Report Tab -----
        report_frame = ttk.Frame(self.report_tab)
        report_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.stockReport = Text(report_frame, width=60, height=15)
        self.stockReport.pack(side="left", fill="both", expand=True)

        report_scroll = ttk.Scrollbar(
            report_frame, orient="vertical", command=self.stockReport.yview
        )
        report_scroll.pack(side="right", fill="y")
        self.stockReport.config(yscrollcommand=report_scroll.set)

        # Main loop
        self.root.mainloop()

    # ----- Functionality -----

    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0, END)
        self.stock_list.clear()
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)
        messagebox.showinfo("Load Data", "Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data", "Data Saved")

    # Refresh history and report tabs when selection changes
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history + report.
    def display_stock_data(self):
        selection = self.stockList.curselection()
        if not selection:
            return

        symbol = self.stockList.get(selection[0])
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel["text"] = f"{stock.name} - {stock.shares} Shares"
                self.dailyDataList.delete("1.0", END)
                self.stockReport.delete("1.0", END)

                self.dailyDataList.insert(
                    END, "- Date -   - Price -   - Volume -\n"
                )
                self.dailyDataList.insert(END, "=================================\n")
                for daily_data in stock.DataList:
                    row = (
                        daily_data.date.strftime("%m/%d/%y")
                        + "   "
                        + "${:0,.2f}".format(daily_data.close)
                        + "   "
                        + str(daily_data.volume)
                        + "\n"
                    )
                    self.dailyDataList.insert(END, row)

                # report summary
                if stock.DataList:
                    latest = stock.DataList[-1]
                    total_value = stock.shares * latest.close
                    self.stockReport.insert(
                        END,
                        f"Symbol: {stock.symbol}\n"
                        f"Name: {stock.name}\n"
                        f"Shares: {stock.shares}\n"
                        f"Last Price: ${latest.close:0.2f}\n"
                        f"Total Value: ${total_value:0.2f}\n",
                    )

                break

    # Add new stock to track.
    def add_stock(self):
        symbol = self.addSymbolEntry.get().strip().upper()
        name = self.addNameEntry.get().strip()
        shares_text = self.addSharesEntry.get().strip()

        if not symbol or not name or not shares_text:
            messagebox.showwarning(
                "Add Stock", "Please fill in Symbol, Name, and Shares."
            )
            return

        try:
            shares = float(shares_text)
        except ValueError:
            messagebox.showerror("Add Stock", "Shares must be a number.")
            return

        new_stock = Stock(symbol, name, shares)
        self.stock_list.append(new_stock)
        self.stockList.insert(END, symbol)

        self.addSymbolEntry.delete(0, END)
        self.addNameEntry.delete(0, END)
        self.addSharesEntry.delete(0, END)

    # Buy shares of stock.
    def buy_shares(self):
        selection = self.stockList.curselection()
        if not selection:
            messagebox.showwarning("Buy Shares", "Please select a stock first.")
            return

        amount_text = self.updateSharesEntry.get().strip()
        if not amount_text:
            messagebox.showwarning("Buy Shares", "Enter number of shares to buy.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Buy Shares", "Shares must be a number.")
            return

        symbol = self.stockList.get(selection[0])
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(amount)
                break

        self.display_stock_data()
        messagebox.showinfo("Buy Shares", "Shares purchased.")
        self.updateSharesEntry.delete(0, END)

    # Sell shares of stock.
    def sell_shares(self):
        selection = self.stockList.curselection()
        if not selection:
            messagebox.showwarning("Sell Shares", "Please select a stock first.")
            return

        amount_text = self.updateSharesEntry.get().strip()
        if not amount_text:
            messagebox.showwarning("Sell Shares", "Enter number of shares to sell.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Sell Shares", "Shares must be a number.")
            return

        symbol = self.stockList.get(selection[0])
        for stock in self.stock_list:
            if stock.symbol == symbol:
                try:
                    stock.sell(amount)
                except Exception as e:
                    messagebox.showerror("Sell Shares", str(e))
                break

        self.display_stock_data()
        messagebox.showinfo("Sell Shares", "Shares sold.")
        self.updateSharesEntry.delete(0, END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
        selection = self.stockList.curselection()
        if not selection:
            messagebox.showwarning(
                "Delete Stock", "Please select a stock to delete."
            )
            return

        index = selection[0]
        symbol = self.stockList.get(index)

        if not messagebox.askyesno("Delete Stock", f"Delete {symbol}?"):
            return

        to_remove = None
        for stock in self.stock_list:
            if stock.symbol == symbol:
                to_remove = stock
                break
        if to_remove:
            self.stock_list.remove(to_remove)

        self.stockList.delete(index)

        self.headingLabel["text"] = "No stock selected"
        self.dailyDataList.delete("1.0", END)
        self.stockReport.delete("1.0", END)

    # Get data from web scraping.
    def scrape_web_data(self):
        if not self.stock_list:
            messagebox.showwarning(
                "Get Data From Web", "Add or load stocks before retrieving data."
            )
            return

        dateFrom = simpledialog.askstring(
            "Starting Date", "Enter Starting Date (m/d/yy)"
        )
        if dateFrom is None:
            return

        dateTo = simpledialog.askstring(
            "Ending Date", "Enter Ending Date (m/d/yy)"
        )
        if dateTo is None:
            return

        try:
            stock_data.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
        except Exception:
            messagebox.showerror(
                "Cannot Get Data from Web", "Check Path for Chrome Driver"
            )
            return

        self.display_stock_data()
        messagebox.showinfo("Get Data From Web", "Data Retrieved")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        selection = self.stockList.curselection()
        if not selection:
            messagebox.showwarning(
                "Import CSV", "Please select a stock first."
            )
            return

        symbol = self.stockList.get(selection[0])
        filename = filedialog.askopenfilename(
            title="Select " + symbol + " File to Import",
            filetypes=[("Yahoo Finance! CSV", "*.csv")],
        )
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list, symbol, filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete", symbol + " Import Complete")

    # Display stock price chart.
    def display_chart(self):
        selection = self.stockList.curselection()
        if not selection:
            messagebox.showwarning(
                "Display Chart", "Please select a stock first."
            )
            return

        symbol = self.stockList.get(selection[0])
        display_stock_chart(self.stock_list, symbol)


def main():
    app = StockApp()


if __name__ == "__main__":
    main()
