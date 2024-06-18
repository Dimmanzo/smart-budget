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

def main():
    while True:
        print("1. Set budget")
        print("2. Add transaction")
        print("3. Update transaction")
        print("4. Delete transaction")
        print("5. View transaction")
        print("6. Generate report")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            pass
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

print("Welcome to Smart Budget!")
main()