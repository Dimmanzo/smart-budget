# Smart Budget

[View live project here!](https://smart-budget-48effdb642a1.herokuapp.com/)

Smart Budget is a user-friendly command-line app designed to help users manage their finances efficiently. 
With this app, you can set spending limits for different categories, keep track of your transactions, and generate detailed financial reports. 
Built with Python, it integrates with Google Sheets to store your data, ensuring it's always safe and easy to access.

## Features

### Existing Features

- __Set Budget__
  - Users can set budget limits for predefined categories (Housing, Transport, Food, Entertainment, Savings).
  - Error handling for invalid inputs and duplicate budget entries.

- __Add Transaction__
  - Allows users to record income and expense transactions.
  - Automatically uses today's date if the user presses enter.
  - Ensures valid input for dates, transaction types, categories, and amounts.
  - Ensures descriptions cannot be left empty.
  - Provides feedback and progress indicators.

- __Update Transaction__
  - Users can update existing transactions by specifying the date.
  - Handles invalid date formats and non-numeric amounts.
  - Allows changing transaction type, category, amount, and description.

- __Delete Transaction__
  - Lists all transactions for a specified date.
  - Allows the user to select which transaction to delete.
  - Includes a confirmation message before deletion.

- __View Transactions__
  - Displays all transaction records.
  - Uses color coding for enhanced readability.

- __Generate Report__
  - Provides a summary of income, expenses, and savings.
  - Compares spending against budget limits.
  - Uses color coding for a better user experience.

### Features to be Added

- __Enhanced Reporting__
  - Include more detailed reports with monthly and yearly summaries.

- __Transaction Categories__
  - Allow users to define custom categories.

## Technologies Used

- __Python__: Main programming language.
- __gspread__: To interact with Google Sheets.
- __Google OAuth__: For authentication.
- __Colorama__: For colored terminal output.
- __Datetime__: For date verification.

## Testing 

| Action | Result | Pass or Fail |
| :-: | :-: | :-: |
| Open application | Welcome message displayed | ✅ |
| Set budget with valid input | Budget set successfully | ✅ |
| Set budget with invalid input | Error message displayed | ✅ |
| Add transaction with valid input | Transaction added successfully | ✅ |
| Add transaction with invalid input | Error message displayed | ✅ |
| Update transaction with valid input | Transaction updated successfully | ✅ |
| Update transaction with invalid input | Error message displayed | ✅ |
| Delete transaction with valid date | Transaction deleted successfully | ✅ |
| Delete transaction with invalid date | Error message displayed | ✅ |
| View transactions | Transactions displayed | ✅ |
| Generate report | Report displayed | ✅ |


## Bugs

### Solved Bugs

- __Duplicate Transactions__: When adding a transaction, duplicates were being created. This was fixed by checking for existing transactions before adding new ones.
- __Date Format Error__: Invalid date formats were causing incorrect inputs. Added error handling to ensure dates are in the correct format.
- __Budget Overwrite__: Users were unable to overwrite existing budgets. Added a confirmation prompt to allow overwriting.

### Unfixed Bugs

- No known unfixed bugs.

## Validator Testing

- __Python Linter__: No errors found when passing through PEP8 linter.
- __gspread__: Ensured no authorization errors with Google Sheets.
- __Colorama__: Verified color output works across different terminal emulators.

## Deployment

The Smart Budget app was deployed on Heroku using [Code Institute P3 template](https://github.com/Code-Institute-Org/p3-template). Follow these steps to deploy the app:

1. __Add Buildpacks__: 
    - Go to the Settings tab of your app on Heroku.
    - Add the following buildpacks in this order:
        1. `heroku/python`
        2. `heroku/nodejs`

2. __Create Config Vars__:
    - In the Settings tab, click on "Reveal Config Vars".
    - Add a Config Var called `PORT` and set its value to `8000`.
    - If you have credentials, create another Config Var called `CREDS` and paste the JSON into the value field.

3. __Connect to GitHub__:
    - In the Deploy tab, connect your GitHub repository to the Heroku app.
    - Select the repository and branch you want to deploy.

4. __Deploy the App__:
    - Scroll down to the "Manual Deploy" section in the Deploy tab.
    - Click "Deploy Branch".

The app should now be deployed and accessible from the [URL](https://smart-budget-48effdb642a1.herokuapp.com/) provided by Heroku.

## Cloning and Forking

### Cloning

- To clone the repository:
  - On GitHub.com, navigate to the main page of the repository.
  - Above the list of files, click Code.
  - Copy the URL for the repository.
  - Type `git clone`, and then paste the URL you copied earlier.
  - Press Enter to create your local clone.

### Forking

- To fork the repository:
  - On GitHub.com, navigate to the main page of the repository.
  - In the top-right corner of the page, click Fork.
  - Under "Owner," select the dropdown menu and click an owner for the forked repository.
  - Click Create fork.

## Credits

### Content

- The application logic and code were written by me with the help of resources found online:
- Primarily through [Google](https://www.google.com/) searches, [Code Institute](https://codeinstitute.net/) training material and documentation for `datetime` and `colorama`.

### Media

- No media files were used in this project.

## Acknowledgements

- Special thanks to the instructors and mentors from [Code Institute](https://codeinstitute.net/) for their guidance and support.
- Thanks to the contributors of the libraries used: `gspread`, `google-auth`, `datetime` and `colorama`.
