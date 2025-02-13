import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls) -> None:
        if not os.path.exists(cls.CSV_FILE):
            pd.DataFrame(columns=cls.COLUMNS).to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date: str, amount: float, category: str, description: str) -> None:
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            csv.DictWriter(csvfile, fieldnames=cls.COLUMNS).writerow(
                {"date": date, "amount": amount, "category": category, "description": description})

    @classmethod
    def get_transactions(cls, start_date: str, end_date: str) -> pd.DataFrame:
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date, end_date = map(lambda x: datetime.strptime(x, cls.FORMAT), [start_date, end_date])
        return df[(df["date"] >= start_date) & (df["date"] <= end_date)]


class FinanceTracker:

    @staticmethod
    def add_transaction() -> None:
        CSV.initialize_csv()
        date = get_date("Enter transaction date (dd-mm-yyyy) or press enter for today's date: ", allow_default=True)
        CSV.add_entry(date, get_amount(), get_category(), get_description())

    @staticmethod
    def view_transactions() -> None:
        start_date, end_date = get_date("Enter start date (dd-mm-yyyy): "), get_date("Enter end date (dd-mm-yyyy): ")
        df = CSV.get_transactions(start_date, end_date)
        if not df.empty:
            print(df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
            total_income, total_expense = df[df["category"] == "Income"]["amount"].sum(), \
                df[df["category"] == "Expense"]["amount"].sum()
            print(
                f"Summary: Total Income: ${total_income:.2f}, Total Expense: ${total_expense:.2f}, Net Savings: ${(total_income - total_expense):.2f}")
            if input("Show plot? (y/n): ").lower() == "y":
                FinanceTracker.plot_transactions(df)
        else:
            logging.info("No transactions found.")

    @staticmethod
    def plot_transactions(df: pd.DataFrame) -> None:
        df.set_index("date", inplace=True)
        income_df, expense_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0), df[
            df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

        plt.figure(figsize=(10, 5))
        plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
        plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Income and Expenses Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()


def main() -> None:
    while True:
        choice = input("\n1. Add transaction\n2. View transactions\n3. Exit\nChoice (1-3): ").strip()
        if choice == "1":
            try:
                FinanceTracker.add_transaction()
            except FinanceError as e:
                logging.error(f"Transaction failed: {e}")
        elif choice == "2":
            try:
                FinanceTracker.view_transactions()
            except FinanceError as e:
                logging.error(f"Failed to fetch transactions: {e}")
        elif choice == "3":
            logging.info("Exiting.")
            break
        else:
            logging.warning("Invalid choice.")


if __name__ == "__main__":
    main()
