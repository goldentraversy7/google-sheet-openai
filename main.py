import os
import gspread
from google.oauth2.service_account import Credentials
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROMPT_TEMPLATE = """
The following is a table of data from a Google Sheet:
{data}

Please provide a summary or insights based on this data.
"""

def authenticate_google_sheets(service_account_file, sheet_id):
    # Authenticate using the service account file
    creds = Credentials.from_service_account_file(service_account_file, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    
    # Open the sheet using its ID
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(0)  # Access the first worksheet
    
    return worksheet

# Fetch all data from Google Sheet as records
def fetch_google_sheet_data(worksheet):
    all_data = worksheet.get_all_values()
    headers = all_data[1]
        # Ensure headers are unique by appending an index to duplicates
    unique_headers = []
    seen = {}
    for header in headers:
        if header in seen:
            seen[header] += 1
            unique_headers.append(f"{header}_{seen[header]}")
        else:
            seen[header] = 0
            unique_headers.append(header)
    
    # Create a DataFrame using the unique headers and the remaining data
    data = all_data[2:]  # Exclude the header row
    
    return pd.DataFrame(data, columns=unique_headers)  # Convert to a DataFrame for easier processing

# Interact with OpenAI ChatGPT API
def get_openai_response(data_frame, api_key, prompt_template):
    client = OpenAI(
        api_key=api_key,  # This is the default and can be omitted
    )
    data_string = data_frame.to_csv(index=False)  # Convert DataFrame to a CSV-like string
    prompt = prompt_template.format(data=data_string)
    
    response = client.chat.completions.create(
        messages=[
                {"role": "system", "content": "You are a data analyst."},
                {"role": "user", "content": prompt}
        ],
        model="gpt-4o",
    )
    
    return response.choices[0].message.content

def write_to_google_sheet(worksheet, data_frame):
    data = [data_frame.columns.values.tolist()] + data_frame.values.tolist()
    worksheet.clear()
    worksheet.update('A1', data)

# Main Script
def main():

    try:
        # Step 1: Authenticate and fetch data
        worksheet = authenticate_google_sheets(SERVICE_ACCOUNT_FILE, GOOGLE_SHEET_ID)
        data_frame = fetch_google_sheet_data(worksheet)
        
        if data_frame.empty:
            print("The Google Sheet is empty.")
            return
        
        # Step 2: Send data to OpenAI and get response
        response = get_openai_response(data_frame, OPENAI_API_KEY, PROMPT_TEMPLATE)
        
        # Step 3: Display response in the terminal
        print("\n--- ChatGPT's Response ---\n")
        print(response)
        
        # Optional: Prepare processed data (e.g., summary as DataFrame)
        #processed_data = pd.DataFrame([{"ChatGPT Response": response}])

        # Write processed results back to Google Sheet
        #write_to_google_sheet(worksheet, processed_data)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
