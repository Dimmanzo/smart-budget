import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime 
from colorama import Fore

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

INCOME_CATEGORIES = {"W": "Wage", "S": "Savings", "O": "Other"}
EXPENSE_CATEGORIES = {"H": "Housing", "T": "Transport", "F": "Food", "E": "Entertainment"}
VALID_CATEGORIES = {"H": "Housing", "T": "Transport", "F": "Food", "E": "Entertainment", "S": "Savings"}


def get_transactions():
    """
    Gets all transaction records from the worksheet.
    Returns the list of transactions.
    """
    worksheet = SHEET.worksheet("transactions")
    transactions = worksheet.get_all_records()
    return transactions


def set_budget():
    """
    Asks the user to enter a category and a budget limit.
    Adds budget data to the 'budget' worksheet.
    Displays an error if the user enters anything other than a number or invalid category.
    Checks if a budget is already set for the chosen category.
    """
    worksheet = SHEET.worksheet("budget")
    budget_data = worksheet.get_all_records()
    existing_categories = {item["Category"] for item in budget_data}

    while True:
        print("-" * 40)
        category_key = input("Enter the category: (H) Housing, (T) Transport, (F) Food, (E) Entertainment, (S) Savings\n").upper()
        if category_key in VALID_CATEGORIES:
            category = VALID_CATEGORIES[category_key]
            break
        else:
            print("Invalid category. Please choose from H (Housing), T (Transport), F (Food), E (Entertainment), S (Savings).")
    
    if category in existing_categories:
        overwrite = input(f"A budget is already set for {category}. Do you want to overwrite it? (Y/N): ").upper()
        if overwrite != 'Y':
            print("Budget not changed.")
            return

    while True:
        print("-" * 40)
        try:
            limit = float(input(f"Enter the budget limit for {category}:\n"))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    if category in existing_categories:
        for i, item in enumerate(budget_data):
            if item["Category"] == category:
                worksheet.update_cell(i + 2, 2, limit)
                break
        print(f"Budget limit for {category} updated to {limit}")
    else:
        worksheet.append_row([category, limit])
        print(f"Budget limit for {category} set to {limit}")


def add_transaction():
    """
    Asks the user to enter transaction details.
    Send all of the information to Google Sheets worksheet.
    Automatically uses today's date if user presses enter.
    Includes error handling, handles single key inputs for transaction type and category selection.
    """
    while True:
        date = input("Enter the date (YYYY-MM-DD) or press 'Enter' for today's date: ")
        if not date:
            date = datetime.today().strftime("%Y-%m-%d")
            break
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    
    while True:
        transaction_type = input("Enter the type (I for Income, E for Expense): ").upper()
        if transaction_type in ["I", "E"]:
            if transaction_type == "I":
                transaction_type = "income"
                categories = INCOME_CATEGORIES
                print("Choose a category: Wage (W), Savings (S), Other (O)")
            else:
                transaction_type = "expense"
                categories = EXPENSE_CATEGORIES
                print("Choose a category: Housing (H), Transport (T), Food (F), Entertainment (E)")
            break
        else:
            print("Invalid type. Please enter I for Income or E for Expense.")
    
    while True:
        category_key = input("Enter the category: ").upper()
        if category_key in categories:
            category = categories[category_key]
            break
        else:
            print(f"Invalid category. Please choose from {', '.join(categories.keys())}.")
    
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


def update_transaction():
    """
    Asks the user to enter the date of the transaction to update.
    Find and updates transaction in 'transactions' worksheet.
    Handles invalid date format, transaction type, category and non-numeric amount.
    """
    while True:
        date = input("Enter the date of the transaction to update (YYYY-MM-DD): ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    transcations = get_transactions()
    worksheet = SHEET.worksheet("transactions")
    for i, transaction in enumerate(transcations):
        if transaction["Date"] == date:
            print(f"Found transaction: {transaction}")
            while True:
                transaction_type = input("Enter the new type (I for Income, E for Expense): ").upper()
                if transaction_type in ["I", "E"]:
                    if transaction_type == "I":
                        transaction_type = "income"
                        categories = INCOME_CATEGORIES
                        print("Choose a new category: Wage (W), Savings (S), Other (O)")
                    else:
                        transaction_type = "expense"
                        categories = EXPENSE_CATEGORIES
                        print("Choose a new category: Housing (H), Transport (T), Food (F), Entertainment (E)")
                    break
                else:
                    print("Invalid type. Please enter I for Income or E for Expense.")

            while True:
               category_key = input("Enter the new category: ").upper()
               if category_key in categories:
                category = categories[category_key]
                break
            else:
                print(f"Invalid category. Please choose from {', '.join(categories.keys())}.") 

            while True:
                try:
                    amount = float(input("Enter the new amount: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a number for the amount.")

            description = input("Enter the new description: ")
            worksheet.update(range_name=f'A{i+2}:E{i+2}', values=[[date, transaction_type, category, amount, description]])
            print("Transaction updated successfully!")
            return
    print("Transaction not found.")


def delete_transaction():
    """
    Prompts the user to enter the date of the transaction to delete.
    Finds and lists all transactions from the 'transactions' worksheet for that date.
    Allows the user to choose which transaction to delete.
    Handles invalid date format and includes a confirmation message before deletion.
    """
    while True:
        date = input("Enter the date of the transaction to delete (YYYY-MM-DD): ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    transactions = get_transactions()
    worksheet = SHEET.worksheet("transactions")

    # Filter transactions by date
    transactions_on_date = [t for t in transactions if t["Date"] == date]

    if not transactions_on_date:
        print("No transactions found on this date.")
        return

    print("Transactions on this date:")
    print("-" * 40)
    for idx, transaction in enumerate(transactions_on_date, start=1):
        print(f"{idx}. Date: {Fore.GREEN}{transaction['Date']}{Fore.RESET} | Type: {Fore.GREEN}{transaction['Type']}{Fore.RESET} | "
              f"Category: {Fore.GREEN}{transaction['Category']}{Fore.RESET} | Amount: {Fore.GREEN}{transaction['Amount']}{Fore.RESET} | "
              f"Description: {Fore.GREEN}{transaction['Description']}{Fore.RESET}")

    while True:
        try:
            transaction_number = int(input("Enter the number of the transaction you want to delete: "))
            if 1 <= transaction_number <= len(transactions_on_date):
                selected_transaction = transactions_on_date[transaction_number - 1]
                break
            else:
                print(f"Invalid number. Please enter a number between 1 and {len(transactions_on_date)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"Selected transaction: Date: {Fore.GREEN}{selected_transaction['Date']}{Fore.RESET} | Type: {Fore.GREEN}{selected_transaction['Type']}{Fore.RESET} | "
          f"Category: {Fore.GREEN}{selected_transaction['Category']}{Fore.RESET} | Amount: {Fore.GREEN}{selected_transaction['Amount']}{Fore.RESET} | "
          f"Description: {Fore.GREEN}{selected_transaction['Description']}{Fore.RESET}")
    confirm = input(f"Are you sure you want to delete this transaction? ({Fore.GREEN}Y{Fore.RESET}/{Fore.RED}N{Fore.RESET}): ").upper()
    if confirm == 'Y':
        # Find the index of the transaction in the original list
        for i, transaction in enumerate(transactions):
            if transaction == selected_transaction:
                worksheet.delete_rows(i + 2)
                print("Transaction deleted successfully!")
                return
    else:
        print("Transaction deletion canceled.")


def view_transactions():
    """
    Fetches and displays all transaction records from the 'transactions' worksheet.
    """
    transactions = SHEET.worksheet("transactions").get_all_records()
    for transaction in transactions:
        print("-" * 40)
        print(f"Date: {Fore.GREEN}{transaction['Date']}{Fore.RESET} | "
            f"Type: {Fore.GREEN}{transaction['Type']}{Fore.RESET} | "
            f"Category: {Fore.GREEN}{transaction['Category']}{Fore.RESET} | "
            f"Amount: {Fore.GREEN}{transaction['Amount']}{Fore.RESET} | "
            f"Description: {Fore.GREEN}{transaction['Description']}{Fore.RESET}"
        )


def generate_report():
    """

    """
    transactions = get_transactions()
    budget_data = SHEET.worksheet("budget").get_all_records()

    income = sum(float(t['Amount']) for t in transactions if t['Type'] == 'income')
    expenses = sum(float(t['Amount']) for t in transactions if t['Type'] == 'expense')
    savings = income - expenses

    print("-" * 40)
    print(f"Total Income: {Fore.GREEN}{income}{Fore.RESET} | Total Expenses: {Fore.RED}{expenses}{Fore.RESET} | Savings: {Fore.CYAN}{savings}{Fore.RESET}")
    
    print("-" * 40)
    print("Budget Summary:")
    print("-" * 40)
    for category in budget_data:
        category_expenses = sum(float(t['Amount']) for t in transactions if t['Category'] == category['Category'] and t['Type'] == 'expense')
        remaining_budget = float(category['Limit']) - category_expenses
        print(f"{category['Category']} | Spent: {Fore.RED}{category_expenses}{Fore.RESET} | Budget Limit: {Fore.GREEN}{category['Limit']}{Fore.RESET} | Remaining: {Fore.CYAN}{remaining_budget}{Fore.RESET}")


def transactions_menu():
    """
    Sub-menu for viewing and editing transactions.
    Provides options to add, delete, view transactions, or go back to the main menu.
    """
    while True:
        print("-" * 40)
        print("Transactions Menu:")
        print("1. Add transaction")
        print("2. Update transaction")
        print("3. Delete transaction")
        print("4. View Transactions")
        print("5. Back")
        print("-" * 40)

        choice = input("Enter your choice: ")
        if choice == "1":
            add_transaction()
        elif choice == "2":
            update_transaction()
        elif choice == "3":
            delete_transaction()
        elif choice == "4":
            view_transactions()    
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    """
    Main function. Handles menu and user choices.
    Provides options to set budget, add transaction, update transaction, delete transaction, view transactions, and generate report.
    """
    while True:
        print("-" * 40)
        print("1. Set budget")
        print("2. View/Edit transactions")
        print("3. Generate report")
        print("4. Exit")
        print("-" * 40)

        choice = input("Enter your choice: ")
        if choice == "1":
            set_budget()
        elif choice == "2":
            transactions_menu()
        elif choice == "3":
            generate_report()    
        elif choice == "4":
            print("-" * 40)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


print("Welcome to Smart Budget!")
main()