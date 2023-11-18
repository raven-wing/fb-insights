import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def dict_to_list(data):
    """Transforms dict to list of lists."""
    return [[date, value] for date, value in data.items()]


def authenticate(scopes):
    creds = Credentials.from_authorized_user_file("token.json", scopes) if os.path.exists("token.json") else None

    if not creds or not creds.valid:
        creds = refresh_credentials(creds, scopes)

    return creds


def refresh_credentials(creds, scopes):
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
        creds = flow.run_local_server(port=0)
        save_credentials(creds)
    return creds


def save_credentials(creds):
    with open("token.json", "w") as token:
        token.write(creds.to_json())


def upload_data(metric_name, data, spreadsheet_id):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = authenticate(scopes)

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Retrieve existing values in the specified range
        range_name = f"{metric_name}!A2:B"
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        existing_values = result.get("values", [])

        # Filter existing values to get only the values in the first column
        existing_first_column_values = [row[0] for row in existing_values]

        # Prepare new values to be added
        values_to_add = dict_to_list(data)
        values_to_add_filtered = [row for row in values_to_add if row[0] not in existing_first_column_values]

        if values_to_add_filtered:
            # If there are new values to add, append them to the sheet
            range_name = f"{metric_name}!A{len(existing_values) + 2}:B"
            body = {"values": values_to_add_filtered}
            result = sheet.values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()

            no_updated = result.get("updates").get("updatedRows")
            print(f"{no_updated} rows appended to {metric_name} sheet.")
        else:
            print("No new rows to add, as they already exist.")
    except Exception as e:
        print(f"Error: {e}")
        return None
