## Requirements of the project

• Authenticate and access a specific Google Sheet using a service account.  
• Fetch all data as records from the sheet.  
• OpenAI ChatGPT API:  
• Send fetched data to ChatGPT with a custom prompt.  
• Process ChatGPT’s response and display results in the terminal.

## Deliverables

Fully functional python script

## Prerequisites

• Google Sheet Service Account  
• Prepared Google Sheet  
• OpenAI Api Key  
• Install Python 3.12

### How to run:

```
1. Install virtual environment to run python script.
python -m venv venv

2. Install required pip packages
pip install -r requirements.txt

3. create .env file and set environment variables

4. run script
python main.py

5. run cronjob
python cronjob.py
```
