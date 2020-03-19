import pickle  # Stores data in a bytecode format. Makes the token file not readable as plaintext
import os.path  # Some useful tools for dealing with file paths
# The google API modules
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Allows read/write access when passed as a permission scope.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets'
]

# The ID of the spreadsheet to write to. Found in the link to the spreadsheet:
# https://docs.google.com/spreadsheets/d/{THE ID IS HERE}/edit?ts=5e72b845#gid=0
SPREADSHEET_ID = "1V3w3s2glsh6_g8FGe_A5o4N4WrqYBOx2Wqw7GmL-7yw"

# The rainge to access. In this case we are using columns A-G in the sheet titled Main
RANGE_NAME = "Main!A:G"

class Sheets:
    """
    The class which manages connecting to google sheets and executing on that.
    """
    # This function is executed when the class is created.
    def __init__(self, credentials_file, token_file):
        creds = None
        # If a token file is already in existence
        if os.path.exists(token_file):
            # Just load that token
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)

        # If that token was not found, or it is expired
        if not creds or not creds.valid:
            # If the token exists and is expired and there is a refresh token
            if creds and creds.expired and creds.refresh_token:
                # Perform a simple token refresh
                creds.refresh(Request())
            else:
                # Otherwise start a local server to download fresh credentials from
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file,
                    SCOPES
                )
                creds = flow.run_local_server(port = 0)

            # Write the new credentials to the token file.
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)

        # Create the service connection and store it as a class attribute.
        self.service = build('sheets', 'v4', credentials = creds)

    # Inserting a user into the Google Sheet
    def append_user(self, user_data):
        # Make the spreadhseet connection
        sheet = self.service.spreadsheets()

        # Format values
        values = [
            [
                user_data['first_name'],
                user_data['last_name'],
                user_data['email'],
                user_data['school'],
                user_data['major'],
                user_data['game_system'],
                user_data['type_of_player']
            ]
        ]

        body = {
            "values": values
        }

        # Insert the information
        result = sheet.values().append(
            spreadsheetId = SPREADSHEET_ID,
            range = RANGE_NAME,
            valueInputOption = 'RAW',
            body = body
        ).execute()
