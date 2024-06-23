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
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
        category_key = input(f"Enter the category: ({Fore.GREEN}H{Fore.RESET}) Housing, ({Fore.GREEN}T{Fore.RESET}) Transport, ({Fore.GREEN}F{Fore.RESET}) Food, ({Fore.GREEN}E{Fore.RESET}) Entertainment, ({Fore.GREEN}S{Fore.RESET}) Savings\n").upper()
        if category_key in VALID_CATEGORIES:
            category = VALID_CATEGORIES[category_key]
            break
        else:
            print(f"{Fore.RED}Invalid category{Fore.RESET}. Please choose from {Fore.GREEN}H{Fore.RESET} (Housing), {Fore.GREEN}T{Fore.RESET} (Transport), {Fore.GREEN}F{Fore.RESET} (Food), {Fore.GREEN}E{Fore.RESET} (Entertainment), {Fore.GREEN}S{Fore.RESET} (Savings).")
    
    if category in existing_categories:
        overwrite = input(f"A budget is already set for {category}. Do you want to overwrite it? ({Fore.GREEN}Y{Fore.RESET}/{Fore.RED}N{Fore.RESET}): ").upper()
        if overwrite != 'Y':
            print("Budget not changed.")
            return

    while True:
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
        try:
            limit = float(input(f"Enter the budget limit for {Fore.GREEN}{category}{Fore.RESET}:\n"))
            if limit <= 0:
                raise ValueError("Budget limit must be a positive number.")
            break
        except ValueError as e:
            print(f"{Fore.RED}Invalid input!{Fore.RESET} Please enter a {Fore.GREEN}positive number.{Fore.RESET}")

    if category in existing_categories:
        for i, item in enumerate(budget_data):
            if item["Category"] == category:
                worksheet.update_cell(i + 2, 2, limit)
                break
        print(f"Budget limit for {Fore.GREEN}{category}{Fore.RESET} updated to {Fore.GREEN}{limit}{Fore.RESET}")
    else:
        worksheet.append_row([category, limit])
        print(f"Budget limit for {Fore.GREEN}{category}{Fore.RESET} set to {Fore.GREEN}{limit}{Fore.RESET}")


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
            print(f"Date set to today's date: {Fore.GREEN}{date}{Fore.RESET}")
            break
        try:
            datetime.strptime(date, "%Y-%m-%d")
            print(f"Date entered: {Fore.GREEN}{date}{Fore.RESET}")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    
    while True:
        transaction_type = input(f"Enter the type: Income ({Fore.GREEN}I{Fore.RESET}), Expense ({Fore.GREEN}E{Fore.RESET}): ").upper()
        if transaction_type in ["I", "E"]:
            if transaction_type == "I":
                transaction_type = "income"
                categories = INCOME_CATEGORIES
                print(f"Choose a category: Wage ({Fore.GREEN}W{Fore.RESET}), Savings ({Fore.GREEN}S{Fore.RESET}), Other ({Fore.GREEN}O{Fore.RESET})")
            else:
                transaction_type = "expense"
                categories = EXPENSE_CATEGORIES
                print(f"Choose a category: Housing ({Fore.GREEN}H{Fore.RESET}), Transport ({Fore.GREEN}T{Fore.RESET}), Food ({Fore.GREEN}F{Fore.RESET}), Entertainment ({Fore.GREEN}E{Fore.RESET})")
            print(f"Transaction type set to: {Fore.GREEN}{transaction_type}{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}Invalid type{Fore.RESET}. Please enter ({Fore.GREEN}I{Fore.RESET}) for Income or ({Fore.GREEN}E{Fore.RESET}) for Expense.")
    
    while True:
        category_key = input("Enter the category: ").upper()
        if category_key in categories:
            category = categories[category_key]
            print(f"Category set to: {Fore.GREEN}{category}{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}Invalid category{Fore.RESET}. Please choose from Wage ({Fore.GREEN}W{Fore.RESET}), Savings ({Fore.GREEN}S{Fore.RESET}), Other ({Fore.GREEN}O{Fore.RESET}).")
    
    while True:
        try:
            amount = float(input("Enter the amount: "))
            if amount <= 0:
                raise ValueError("Amount must be a positive number.")
            print(f"Amout set to: {Fore.GREEN}{amount}{Fore.RESET}")
            break
        except ValueError as e:
            print(f"{Fore.RED}Invalid input!{Fore.RESET} Please enter a positive number.")

    while True:
        description = input("Enter the description: ")
        if description.strip():
            print(f"Description entered: {Fore.GREEN}{description}{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}Description cannot be empty{Fore.RESET}. Please enter a valid description.")

    worksheet = SHEET.worksheet("transactions")
    worksheet.append_row([date, transaction_type, category, amount, description])
    print(f"{Fore.GREEN}Transaction added successfully!{Fore.RESET}")


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
            print(f"Date entered: {Fore.GREEN}{date}{Fore.RESET}")
            break
        except ValueError:
            print(f"{Fore.RED}Invalid date format{Fore.RESET}. Please enter the date in YYYY-MM-DD format.")

    transcations = get_transactions()
    worksheet = SHEET.worksheet("transactions")
    for i, transaction in enumerate(transcations):
        if transaction["Date"] == date:
            print(f"Found transaction: {Fore.GREEN}{transaction}{Fore.RESET}")
            while True:
                transaction_type = input(f"Enter the new type ({Fore.GREEN}I{Fore.RESET}) Income, ({Fore.GREEN}E{Fore.RESET}) Expense: ").upper()
                if transaction_type in ["I", "E"]:
                    if transaction_type == "I":
                        transaction_type = "income"
                        categories = INCOME_CATEGORIES
                        print(f"Choose a new category: Wage ({Fore.GREEN}W{Fore.RESET}), Savings ({Fore.GREEN}S{Fore.RESET}), Other ({Fore.GREEN}O{Fore.RESET})")
                    else:
                        transaction_type = "expense"
                        categories = EXPENSE_CATEGORIES
                        print(f"Choose a new category: Housing ({Fore.GREEN}H{Fore.RESET}), Transport ({Fore.GREEN}T{Fore.RESET}), Food ({Fore.GREEN}F{Fore.RESET}), Entertainment ({Fore.GREEN}E{Fore.RESET})")
                    print(f"Transaction type set to: {Fore.GREEN}{transaction_type}{Fore.RESET}")
                    break
                else:
                    print(f"{Fore.RED}Invalid type{Fore.RESET}. Please enter ({Fore.GREEN}I{Fore.RESET}) Income or ({Fore.GREEN}E{Fore.RESET}) Expense.")

            while True:
               category_key = input("Enter the new category: ").upper()
               if category_key in categories:
                category = categories[category_key]
                print(f"Category set to: {Fore.GREEN}{category}{Fore.RESET}")
                break
            else:
                print(f"{Fore.RED}Invalid category{Fore.RESET}. Please choose from {', '.join(categories.keys())}.") 

            while True:
                try:
                    amount = float(input("Enter the new amount: "))
                    if amount <= 0:
                        raise ValueError("Amount must be a positive number.")
                    print(f"Amount set to: {Fore.GREEN}{amount}{Fore.RESET}")
                    break
                except ValueError as e:
                    print(f"{Fore.RED}Invalid input!{Fore.RESET} {e} Please enter a number for the amount.")

            while True:
                description = input("Enter the new description: ")
                if description.strip():
                    print(f"Description entered: {Fore.GREEN}{description}{Fore.RESET}")
                    break
                else:
                    print(f"{Fore.RED}Description cannot be empty{Fore.RESET}. Please enter a valid description.")

            worksheet.update(range_name=f'A{i+2}:E{i+2}', values=[[date, transaction_type, category, amount, description]])
            print(f"{Fore.GREEN}Transaction updated successfully!{Fore.RESET}")
            return
    print(f"{Fore.RED}Transaction not found.{Fore.RESET}")


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
            print(f"Date entered: {Fore.GREEN}{date}{Fore.RESET}")
            break
        except ValueError:
            print(f"{Fore.RED}Invalid date format{Fore.RESET}. Please enter the date in YYYY-MM-DD format.")

    transactions = get_transactions()
    worksheet = SHEET.worksheet("transactions")

    # Filter transactions by date
    transactions_on_date = [t for t in transactions if t["Date"] == date]

    if not transactions_on_date:
        print(f"{Fore.RED}No transactions found on this date.{Fore.RESET}")
        return

    print("Transactions on this date:")
    print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
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
                print(f"{Fore.RED}Invalid number{Fore.RESET}. Please enter a number between {Fore.GREEN}1{Fore.RESET} and {Fore.GREEN}{len(transactions_on_date)}{Fore.RESET}.")
        except ValueError:
            print(f"{Fore.RED}Invalid input{Fore.RESET}. Please enter a number.")

    print(f"Selected transaction: Date: {Fore.GREEN}{selected_transaction['Date']}{Fore.RESET} | Type: {Fore.GREEN}{selected_transaction['Type']}{Fore.RESET} | "
          f"Category: {Fore.GREEN}{selected_transaction['Category']}{Fore.RESET} | Amount: {Fore.GREEN}{selected_transaction['Amount']}{Fore.RESET} | "
          f"Description: {Fore.GREEN}{selected_transaction['Description']}{Fore.RESET}")
    confirm = input(f"Are you sure you want to delete this transaction? ({Fore.GREEN}Y{Fore.RESET}/{Fore.RED}N{Fore.RESET}): ").upper()
    if confirm == 'Y':
        # Find the index of the transaction in the original list
        for i, transaction in enumerate(transactions):
            if transaction == selected_transaction:
                worksheet.delete_rows(i + 2)
                print(f"{Fore.GREEN}Transaction deleted successfully{Fore.RESET}!")
                return
    else:
        print(f"{Fore.RED}Transaction deletion canceled{Fore.RESET}.")


def view_transactions():
    """
    Fetches and displays all transaction records from the 'transactions' worksheet.
    """
    transactions = SHEET.worksheet("transactions").get_all_records()
    for transaction in transactions:
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
        print(f"Date: {Fore.GREEN}{transaction['Date']}{Fore.RESET} | "
            f"Type: {Fore.GREEN}{transaction['Type']}{Fore.RESET} | "
            f"Category: {Fore.GREEN}{transaction['Category']}{Fore.RESET} | "
            f"Amount: {Fore.GREEN}{transaction['Amount']}{Fore.RESET} | "
            f"Description: {Fore.GREEN}{transaction['Description']}{Fore.RESET}"
        )


def generate_report():
    """
    Generates and displays a financial report based on the transactions and budget data.
    Calculates total income, expenses, savings, and compares spending against budget limits.
    Uses colorama for colored output to enhance user experience.
    """
    transactions = get_transactions()
    budget_data = SHEET.worksheet("budget").get_all_records()

    income = sum(float(t['Amount']) for t in transactions if t['Type'] == 'income')
    expenses = sum(float(t['Amount']) for t in transactions if t['Type'] == 'expense')
    savings = income - expenses

    print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
    print(f"Total Income: {Fore.GREEN}{income}{Fore.RESET} | Total Expenses: {Fore.RED}{expenses}{Fore.RESET} | Savings: {Fore.CYAN}{savings}{Fore.RESET}")
    
    print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
    print("Budget Summary:")
    print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
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
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
        print("Transactions Menu:")
        print(f"{Fore.GREEN}1{Fore.RESET}. Add transaction")
        print(f"{Fore.GREEN}2{Fore.RESET}. Update transaction")
        print(f"{Fore.GREEN}3{Fore.RESET}. Delete transaction")
        print(f"{Fore.GREEN}4{Fore.RESET}. View Transactions")
        print(f"{Fore.GREEN}5{Fore.RESET}. Back")
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)

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
            print(f"{Fore.GREEN}Invalid choice{Fore.RESET}. Please try again.")

def main():
    """
    Main function. Handles menu and user choices.
    Provides options to set budget, add transaction, update transaction, delete transaction, view transactions, and generate report.
    """
    while True:
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
        print(f"{Fore.GREEN}1{Fore.RESET}. Set budget")
        print(f"{Fore.GREEN}2{Fore.RESET}. View/Edit transactions")
        print(f"{Fore.GREEN}3{Fore.RESET}. Generate report")
        print(f"{Fore.GREEN}4{Fore.RESET}. Exit")
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)

        choice = input("Enter your choice: ")
        if choice == "1":
            set_budget()
        elif choice == "2":
            transactions_menu()
        elif choice == "3":
            generate_report()    
        elif choice == "4":
            print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
            print("Goodbye!")
            break
        else:
            print(f"{Fore.RED}Invalid choice{Fore.RESET}. Please try again.")


print(f"Welcome to {Fore.GREEN}Smart Budget{Fore.RESET}!")
main()