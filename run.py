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

"""
Asks the user to enter a category and a budget limit.
Adds budget data to the 'budget' worksheet.
Displays an error if the user enters anything other than a number or invalid category.
"""
def set_budget():
    while True:
        category = input("Enter the category (Housing, Transport, Food, Entertainment, Savings):\n")
        if category in VALID_CATEGORIES:
            break
        else:
            print("Invalid category. Please choose from Housing, Transport, Food, Entertainment, Savings.")
    while True:
        try:
            limit = float(input(f"Enter the budget limit for {category}:\n"))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    worksheet = SHEET.worksheet("budget")
    worksheet.append_row([category, limit])
    print(f"Budget limit for {category} set to {limit}")


"""
Main function. Handles menu and user choices.
Provides options to set budget, add transaction, update transaction, delete transaction, view transactions, and generate report.
"""
def main():
    while True:
        print("1. Set budget")
        print("2. Add transaction")
        print("3. Update transaction")
        print("4. Delete transaction")
        print("5. View transaction")
        print("6. Generate report")
        print("7. Exit")

        choice = input("\nEnter your choice: ")
        if choice == "1":
            set_budget()
        elif choice == "2":
            pass
        elif choice == "3":
            pass  
        elif choice == "4":
            pass 
        elif choice == "5":
            pass  
        elif choice == "6":
            pass  
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

print("Welcome to Smart Budget!\n")
main()