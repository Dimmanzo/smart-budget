import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime 
from colorama import Fore

# Google Sheets configuration
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Credentials and client setup
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('smart-budget')

# Categories for transactions
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

    # Prompt for category
    while True:
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
        category_key = input(f"Enter the category: ({Fore.GREEN}H{Fore.RESET}) Housing, ({Fore.GREEN}T{Fore.RESET}) Transport, ({Fore.GREEN}F{Fore.RESET}) Food, ({Fore.GREEN}E{Fore.RESET}) Entertainment, ({Fore.GREEN}S{Fore.RESET}) Savings\n").upper()
        if category_key in VALID_CATEGORIES:
            category = VALID_CATEGORIES[category_key]
            break
        else:
            print(f"{Fore.RED}Invalid category{Fore.RESET}. Please choose from {Fore.GREEN}H{Fore.RESET} (Housing), {Fore.GREEN}T{Fore.RESET} (Transport), {Fore.GREEN}F{Fore.RESET} (Food), {Fore.GREEN}E{Fore.RESET} (Entertainment), {Fore.GREEN}S{Fore.RESET} (Savings).")
    
    # Check for existing budget
    if category in existing_categories:
        overwrite = input(f"A budget is already set for {Fore.GREEN}{category}{Fore.RESET}. Do you want to overwrite it? ({Fore.GREEN}Y{Fore.RESET}/{Fore.RED}N{Fore.RESET}):\n").upper()
        if overwrite != 'Y':
            print(f"{Fore.GREEN}Budget not changed{Fore.RESET}.")
            return
    
    # Prompt for budget limit
    while True:
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
        try:
            limit = float(input(f"Enter the budget limit for {Fore.GREEN}{category}{Fore.RESET}:\n"))
            if limit <= 0:
                raise ValueError(f"Budget limit must be a {Fore.GREEN}positive number{Fore.RESET}.")
            break
        except ValueError as e:
            print(f"{Fore.RED}Invalid input!{Fore.RESET} Please enter a {Fore.GREEN}positive number.{Fore.RESET}")

    # Update or add budget
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
    # Prompt for date
    while True:
        date = input(f"Enter the date ({Fore.GREEN}YYYY-MM-DD{Fore.RESET}) or press '{Fore.GREEN}Enter{Fore.RESET}' for today's date:\n")
        if not date:
            date = datetime.today().strftime("%Y-%m-%d")
            print(f"Date set to today's date: {Fore.GREEN}{date}{Fore.RESET}")
            break
        try:
            datetime.strptime(date, "%Y-%m-%d")
            print(f"Date entered: {Fore.GREEN}{date}{Fore.RESET}")
            break
        except ValueError:
            print(f"{Fore.RED}Invalid date format{Fore.RESET}. Please enter the date in {Fore.GREEN}YYYY-MM-DD{Fore.RESET} format.")
    
    # Prompt for transaction type
    while True:
        transaction_type = input(f"Enter the type: ({Fore.GREEN}I{Fore.RESET}) Income, ({Fore.GREEN}E{Fore.RESET}) Expense:\n").upper()
        if transaction_type in ["I", "E"]:
            if transaction_type == "I":
                transaction_type = "income"
                categories = INCOME_CATEGORIES
                print(f"Choose a category: ({Fore.GREEN}W{Fore.RESET}) Wage, ({Fore.GREEN}S{Fore.RESET}) Savings, ({Fore.GREEN}O{Fore.RESET}) Other:")
            else:
                transaction_type = "expense"
                categories = EXPENSE_CATEGORIES
            print(f"Transaction type set to: {Fore.GREEN}{transaction_type}{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}Invalid type{Fore.RESET}. Please enter ({Fore.GREEN}I{Fore.RESET}) for Income or ({Fore.GREEN}E{Fore.RESET}) for Expense.")
    
    # Prompt for category
    if transaction_type == "income":
        print(f"Choose a category: ({Fore.GREEN}W{Fore.RESET}) Wage, ({Fore.GREEN}S{Fore.RESET}) Savings, ({Fore.GREEN}O{Fore.RESET}) Other:")
    else:
        print(f"Choose a category: ({Fore.GREEN}H{Fore.RESET}) Housing, ({Fore.GREEN}T{Fore.RESET}) Transport, ({Fore.GREEN}F{Fore.RESET}) Food, ({Fore.GREEN}E{Fore.RESET}) Entertainment")

    while True:
        category_key = input("Enter the category:\n").upper()
        if category_key in categories:
            category = categories[category_key]
            print(f"Category set to: {Fore.GREEN}{category}{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}Invalid category{Fore.RESET}. Please choose from Wage ({Fore.GREEN}W{Fore.RESET}), Savings ({Fore.GREEN}S{Fore.RESET}), Other ({Fore.GREEN}O{Fore.RESET}).")
    
    # Prompt for amount
    while True:
        try:
            amount = float(input("Enter the amount:\n"))
            if amount <= 0:
                raise ValueError(f"Amount must be a {Fore.GREEN}positive number{Fore.RESET}.")
            print(f"Amout set to: {Fore.GREEN}{amount}{Fore.RESET}")
            break
        except ValueError as e:
            print(f"{Fore.RED}Invalid input!{Fore.RESET} Please enter a {Fore.GREEN}positive number{Fore.RESET}.")

    # Prompt for description
    while True:
        description = input("Enter the description:\n")
        if description.strip():
            print(f"Description entered: {Fore.GREEN}{description}{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}Description cannot be empty{Fore.RESET}. Please enter a valid description.")

    # Display transaction summary
    print(f"\nTransaction Summary - Date: {Fore.GREEN}{date}{Fore.RESET} | Type: {Fore.GREEN}{transaction_type}{Fore.RESET} | "
          f"Category: {Fore.GREEN}{category}{Fore.RESET} | Amount: {Fore.GREEN}{amount}{Fore.RESET} | Description: {Fore.GREEN}{description}{Fore.RESET}\n")

    # Confirm save
    while True:
        confirm = input(f"Do you want to save this transaction? ({Fore.GREEN}Y{Fore.RESET}/{Fore.RED}N{Fore.RESET}): ").upper()
        if confirm == 'Y':
            worksheet = SHEET.worksheet("transactions")
            worksheet.append_row([date, transaction_type, category, amount, description])
            print(f"{Fore.GREEN}Transaction added successfully!{Fore.RESET}")
            break
        elif confirm == 'N':
            print(f"{Fore.RED}Transaction not saved.{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}Invalid choice{Fore.RESET}. Please enter ({Fore.GREEN}Y{Fore.RESET}) to save or ({Fore.RED}N{Fore.RESET}) to cancel.")


def update_transaction():
    """
    Asks the user to enter the date of the transaction to update.
    Find and updates transaction in 'transactions' worksheet.
    Handles invalid date format, transaction type, category and non-numeric amount.
    """
    # Prompt for date
    while True:
        date = input(f"Enter the date of the transaction to update ({Fore.GREEN}YYYY-MM-DD{Fore.RESET}):\n")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            print(f"Date entered: {Fore.GREEN}{date}{Fore.RESET}")
            break
        except ValueError:
            print(f"{Fore.RED}Invalid date format{Fore.RESET}. Please enter the date in {Fore.GREEN}YYYY-MM-DD{Fore.RESET} format.")

    # Fetch transactions
    transcations = get_transactions()
    worksheet = SHEET.worksheet("transactions")
    for i, transaction in enumerate(transcations):
        if transaction["Date"] == date:
            print(f"Found transaction: {Fore.GREEN}{transaction}{Fore.RESET}")
            # Prompt for new transaction type
            while True:
                transaction_type = input(f"Enter the new type ({Fore.GREEN}I{Fore.RESET}) Income, ({Fore.GREEN}E{Fore.RESET}) Expense:\n").upper()
                if transaction_type in ["I", "E"]:
                    if transaction_type == "I":
                        transaction_type = "income"
                        categories = INCOME_CATEGORIES
                        print(f"Choose a new category: ({Fore.GREEN}W{Fore.RESET}) Wage, ({Fore.GREEN}S{Fore.RESET}) Savings, ({Fore.GREEN}O{Fore.RESET}) Other")
                    else:
                        transaction_type = "expense"
                        categories = EXPENSE_CATEGORIES
                        print(f"Choose a new category: ({Fore.GREEN}H{Fore.RESET}) Housing, ({Fore.GREEN}T{Fore.RESET}) Transport, ({Fore.GREEN}F{Fore.RESET}) Food, ({Fore.GREEN}E{Fore.RESET}) Entertainment")
                    print(f"Transaction type set to: {Fore.GREEN}{transaction_type}{Fore.RESET}")
                    break
                else:
                    print(f"{Fore.RED}Invalid type{Fore.RESET}. Please enter ({Fore.GREEN}I{Fore.RESET}) Income or ({Fore.GREEN}E{Fore.RESET}) Expense.")

            # Prompt for new category
            while True:
               category_key = input("Enter the new category:\n").upper()
               if category_key in categories:
                category = categories[category_key]
                print(f"Category set to: {Fore.GREEN}{category}{Fore.RESET}")
                break
            else:
                print(f"{Fore.RED}Invalid category{Fore.RESET}. Please choose from {Fore.GREEN}{', '.join(categories.keys())}{Fore.RESET}.") 

            # Prompt for new amount
            while True:
                try:
                    amount = float(input("Enter the new amount:\n"))
                    if amount <= 0:
                        raise ValueError(f"Amount must be a {Fore.GREEN}positive number{Fore.RESET}.")
                    print(f"Amount set to: {Fore.GREEN}{amount}{Fore.RESET}")
                    break
                except ValueError as e:
                    print(f"{Fore.RED}Invalid input!{Fore.RESET} {e} Please enter a number for the amount.")

            # Prompt for new description
            while True:
                description = input("Enter the new description:\n")
                if description.strip():
                    print(f"Description entered: {Fore.GREEN}{description}{Fore.RESET}")
                    break
                else:
                    print(f"{Fore.RED}Description cannot be empty{Fore.RESET}. Please enter a valid description.")
            
            # Update transaction
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
    # Prompt for date
    while True:
        date = input(f"Enter the date of the transaction to delete ({Fore.GREEN}YYYY-MM-DD{Fore.RESET}):\n")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            print(f"Date entered: {Fore.GREEN}{date}{Fore.RESET}")
            break
        except ValueError:
            print(f"{Fore.RED}Invalid date format{Fore.RESET}. Please enter the date in {Fore.GREEN}YYYY-MM-DD{Fore.RED} format.")

    # Fetch transactions and filter by date
    transactions = get_transactions()
    worksheet = SHEET.worksheet("transactions")
    transactions_on_date = [t for t in transactions if t["Date"] == date]

    if not transactions_on_date:
        print(f"{Fore.RED}No transactions found on this date.{Fore.RESET}")
        return
    
    # Display transactions on selected date
    print("Transactions on this date:")
    print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
    for idx, transaction in enumerate(transactions_on_date, start=1):
        print(f"{idx}. Date: {Fore.GREEN}{transaction['Date']}{Fore.RESET} | Type: {Fore.GREEN}{transaction['Type']}{Fore.RESET} | "
              f"Category: {Fore.GREEN}{transaction['Category']}{Fore.RESET} | Amount: {Fore.GREEN}{transaction['Amount']}{Fore.RESET} | "
              f"Description: {Fore.GREEN}{transaction['Description']}{Fore.RESET}")

    # Prompt for transaction number to delete
    while True:
        try:
            transaction_number = int(input("Enter the number of the transaction you want to delete:\n"))
            if 1 <= transaction_number <= len(transactions_on_date):
                selected_transaction = transactions_on_date[transaction_number - 1]
                break
            else:
                print(f"{Fore.RED}Invalid number{Fore.RESET}. Please enter a number between {Fore.GREEN}1{Fore.RESET} and {Fore.GREEN}{len(transactions_on_date)}{Fore.RESET}.")
        except ValueError:
            print(f"{Fore.RED}Invalid input{Fore.RESET}. Please enter a number.")

    # Confirm deletion
    print(f"Selected transaction: Date: {Fore.GREEN}{selected_transaction['Date']}{Fore.RESET} | Type: {Fore.GREEN}{selected_transaction['Type']}{Fore.RESET} | "
          f"Category: {Fore.GREEN}{selected_transaction['Category']}{Fore.RESET} | Amount: {Fore.GREEN}{selected_transaction['Amount']}{Fore.RESET} | "
          f"Description: {Fore.GREEN}{selected_transaction['Description']}{Fore.RESET}")
    confirm = input(f"Are you sure you want to delete this transaction? ({Fore.GREEN}Y{Fore.RESET}/{Fore.RED}N{Fore.RESET}): ").upper()
    if confirm == 'Y':
        # Find the index of the transaction and delete.
        for i, transaction in enumerate(transactions):
            if transaction == selected_transaction:
                worksheet.delete_rows(i + 2)
                print(f"{Fore.GREEN}Transaction deleted successfully{Fore.RESET}!")
                return
    else:
        print(f"{Fore.RED}Transaction deletion canceled{Fore.RESET}.")


def view_transactions():
    """
    Fetches and displays all transaction records from the 'transactions' worksheet
    for a specific month or year based on user input.
    """
    # Prompt for view option
    while True:
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
        print(f"{Fore.GREEN}1{Fore.RESET}. View transactions ({Fore.GREEN}Month{Fore.RESET})")
        print(f"{Fore.GREEN}2{Fore.RESET}. View transactions ({Fore.GREEN}Year{Fore.RESET})")
        print(f"{Fore.GREEN}3{Fore.RESET}. Back")
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
 
        # Handle user choice
        choice = input("Enter your choice:\n")
        if choice == "1":
            date_format = "%Y-%m"
            promt = f"Enter the month and year ({Fore.GREEN}YYYY-MM{Fore.RESET}):\n"
            break
        elif choice == "2":
            date_format = "%Y"
            promt = f"Enter the year ({Fore.GREEN}YYYY{Fore.RESET}):\n"
            break
        elif choice == "3":
            return
        else:
            print(f"{Fore.RED}Invalid choice{Fore.RESET}. Please try again.")

    # Prompt for date input
    while True:
        date_input = input(promt)
        try:
            selected_date = datetime.strptime(date_input, date_format)
            break
        except ValueError:
            print(f"{Fore.RED}Invalid date format{Fore.RESET}. Please enter the date in {Fore.GREEN}{date_format}{Fore.RESET} format.")

    # Fetch and filter transactions
    transactions = get_transactions()
    filtered_transactions = []
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction['Date'], "%Y-%m-%d")
        if date_format == "%Y-%m" and transaction_date.strftime("%Y-%m") == selected_date.strftime("%Y-%m"):
            filtered_transactions.append(transaction)
        if date_format == "%Y" and transaction_date.strftime("%Y") == selected_date.strftime("%Y"):
            filtered_transactions.append(transaction)

    # Display filtered transactions
    if not filtered_transactions:
        print(f"{Fore.RED}No transactions found for the selected period.{Fore.RESET}")
        return

    for transaction in filtered_transactions:
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
        print(f"Date: {Fore.GREEN}{transaction['Date']}{Fore.RESET} | "
            f"Type: {Fore.GREEN}{transaction['Type']}{Fore.RESET} | "
            f"Category: {Fore.GREEN}{transaction['Category']}{Fore.RESET} | "
            f"Amount: {Fore.GREEN}{transaction['Amount']}{Fore.RESET} | "
            f"Description: {Fore.GREEN}{transaction['Description']}{Fore.RESET}")


def generate_report():
    """
    Generates and displays a financial report based on the transactions and budget data.
    Calculates total income, expenses, savings, and compares spending against budget limits.
    Uses colorama for colored output to enhance user experience.
    """
    # Fetch transactions and budget data
    transactions = get_transactions()
    budget_data = SHEET.worksheet("budget").get_all_records()

    # Calculate totals
    income = sum(float(t['Amount']) for t in transactions if t['Type'] == 'income')
    expenses = sum(float(t['Amount']) for t in transactions if t['Type'] == 'expense')
    savings = income - expenses
    
    # Display report
    print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
    print(f"Total Income: {Fore.GREEN}{income}{Fore.RESET} | Total Expenses: {Fore.RED}{expenses}{Fore.RESET} | Savings: {Fore.CYAN}{savings}{Fore.RESET}")
    
     # Display budget summary
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
    # Display menu options
    while True:
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
        print("Transactions Menu:")
        print(f"{Fore.GREEN}1{Fore.RESET}. Add transaction")
        print(f"{Fore.GREEN}2{Fore.RESET}. Update transaction")
        print(f"{Fore.GREEN}3{Fore.RESET}. Delete transaction")
        print(f"{Fore.GREEN}4{Fore.RESET}. View Transactions")
        print(f"{Fore.GREEN}5{Fore.RESET}. Back")
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)

        # Handle user choice
        choice = input("Enter your choice:\n")
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
    # Display main menu options
    while True:
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)
        print(f"{Fore.GREEN}1{Fore.RESET}. Set budget")
        print(f"{Fore.GREEN}2{Fore.RESET}. View/Edit transactions")
        print(f"{Fore.GREEN}3{Fore.RESET}. Generate report")
        print(f"{Fore.GREEN}4{Fore.RESET}. Exit")
        print(f"{Fore.CYAN}-{Fore.RESET}" * 40)

        # Handle user choice
        choice = input("Enter your choice:\n")
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

# Welcome message and start main function
print(f"Welcome to {Fore.GREEN}Smart Budget{Fore.RESET}!")
main()