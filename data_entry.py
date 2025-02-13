from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    date_str = input(prompt) or (datetime.today().strftime(date_format) if allow_default else None)
    if date_str:
        try:
            return datetime.strptime(date_str, date_format).strftime(date_format)
        except ValueError:
            print("Invalid date format. Please use dd-mm-yyyy.")
    else:
        print("Date is required.")
    return get_date(prompt, allow_default)


def get_amount():
    while True:
        try:
            amount = float(input("Enter the amount: "))
            if amount > 0:
                return amount
            else:
                raise ValueError("Amount must be positive.")
        except ValueError as e:
            print(e)


def get_category():
    while True:
        category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
        if category in CATEGORIES:
            return CATEGORIES[category]
        print("Invalid input. Use 'I' for Income or 'E' for Expense.")


def get_description():
    return input("Enter a description (optional): ")
