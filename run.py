import gspread
from google.oauth2.service_account import Credentials

# Google Sheets
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('smart-budget')

VALID_CATEGORIES = ["Housing", "Transport", "Food", "Entertainment", "Savings"]


def set_budget():
    """
    Asks the user to enter a category and a budget limit.
    Adds budget data to the 'budget' worksheet.
    Displays an error if the user enters anything other than a number or invalid category.
    """
    while True:
        print("-" * 40)
        category = input("Enter the category (Housing, Transport, Food, Entertainment, Savings):\n")
        if category in VALID_CATEGORIES:
            break
        else:
            print("Invalid category. Please choose from Housing, Transport, Food, Entertainment, Savings.")
    while True:
        print("-" * 40)
        try:
            limit = float(input(f"Enter the budget limit for {category}:\n"))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    worksheet = SHEET.worksheet("budget")
    worksheet.append_row([category, limit])
    print(f"Budget limit for {category} set to {limit}")


def add_transaction():
    """
    Asks the user to enter transaction details.
    Send all of the information to Google Sheets worksheet.
    Includes error handling: transaction type, category, amount.
    """
    while True:
        date = input("Enter the date (YYYY-MM-DD): ")
        if len(date) == 10 and date[4] == '-' and date[7] == '-':
            break
        else:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    
    while True:
        transaction_type = input("Enter the type (Income/Expense): ")
        if transaction_type in ["Income", "Expense"]:
            break
        else:
            print("Invalid type. Please enter either 'Income' or 'Expense'.")
    
    while True:
        category = input("Enter the category (Housing, Transport, Food, Entertainment, Savings): ")
        if category in VALID_CATEGORIES:
            break
        else:
            print("Invalid category. Please choose from Housing, Transport, Food, Entertainment, Savings.")
    
    while True:
        try:
            amount = float(input("Enter the amount: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    description = input("Enter the description: ")
    worksheet = SHEET.worksheet("transactions")
    worksheet.append_row([date, transaction_type, category, amount, description])
    print("Transaction added successfully!")


def view_transactions():
    """
    Fetches and displays all transaction records from the 'transactions' worksheet.
    """
    transactions = SHEET.worksheet("transactions").get_all_records()
    for transaction in transactions:
        print("-" * 40)
        print(f"Date: {transaction['Date']}")
        print(f"Type: {transaction['Type']}")
        print(f"Category: {transaction['Category']}")
        print(f"Amount: {transaction['Amount']}")
        print(f"Description: {transaction['Description']}")
        print("-" * 40)


def main():
    """
    Main function. Handles menu and user choices.
    Provides options to set budget, add transaction, update transaction, delete transaction, view transactions, and generate report.
    """
    while True:
        print("-" * 40)
        print("1. Set budget")
        print("2. Add transaction")
        print("3. Update transaction")
        print("4. Delete transaction")
        print("5. View transaction")
        print("6. Generate report")
        print("7. Exit")
        print("-" * 40)

        choice = input("Enter your choice: ")
        if choice == "1":
            set_budget()
        elif choice == "2":
            add_transaction()
        elif choice == "3":
            pass  
        elif choice == "4":
            pass 
        elif choice == "5":
            view_transactions()  
        elif choice == "6":
            pass  
        elif choice == "7":
            print("-" * 40)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

print("Welcome to Smart Budget!")
main()