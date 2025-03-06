
# ZF Volunteer Hours Tracker
Command to make app:
 pyinstaller --onefile --noconsole --hidden-import pandas --hidden-import openpyxl app.py

## Google Sheets Integration

This application can store data in either a local CSV file or in Google Sheets. 
To use Google Sheets, follow these steps:

1. Create a Google Cloud project at https://console.cloud.google.com/
2. Enable the Google Sheets API for your project
3. Create OAuth credentials (Desktop application type)
4. Download the credentials JSON file
5. Run the setup utility: From the application menu, select "Google Sheets > Setup Google Sheets"
6. In the setup utility:
   - Select the downloaded credentials file
   - Click "Authenticate with Google" (a browser will open for authentication)
   - To create a new spreadsheet, leave the Spreadsheet ID field empty and click "Create/Select Spreadsheet"
   - To use an existing spreadsheet, enter its ID and click "Create/Select Spreadsheet"
7. Restart the application to use Google Sheets

## Using the Application

- Add volunteers by clicking "Don't See Your Name?"
- Click on a person's name to view their information
- To add volunteer hours, click on a person and fill in the information form
- Administrators can access additional features by entering the admin password

## Data Management

- Export data to CSV using File > Export to CSV
- Import data from CSV using File > Import from CSV (requires admin password)
- Switch between Google Sheets and local storage using Google Sheets > Setup Google Sheets
