import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.

def authenticate():
  creds = None

  if os.path.exists("./google_api/token.json"):
    creds = Credentials.from_authorized_user_file("./google_api/token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "./google_api/client_secret.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    
    with open("./google_api/token.json", "w") as token:
      token.write(creds.to_json())
  
  return creds