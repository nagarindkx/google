from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

"""
Developer: Kanakorn Horsiritham
Organization: Computer Center, Prince of Songkla University
Base Code: Python Quickstart (Google Sheets API v4)
	   https://developers.google.com/sheets/api/quickstart/python
"""

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument("--data", help="CSV format", required=True)
    parser.add_argument("--sheetid", help="Google Sheets ID", required=True)
    parser.add_argument("--range", help="Simply Sheet Name like 'Sheet1!A1'", default="Sheet1!A1")
    parser.add_argument("--value-input-option" ,dest='valueInputOption', help="Optional: [RAW,USER_ENTERED]", default="RAW")
    flags  = parser.parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
    credential_dir = os.getcwd()
    credential_path = os.path.join(credential_dir,
                                   'sheet_credential.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = flags.sheetid
    rangeName = flags.range
    value_input_option = flags.valueInputOption
    insert_data_option = 'INSERT_ROWS' 
    arr = flags.data.split(",")
    value={"values":[ arr ]}
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range=rangeName, valueInputOption=value_input_option ,insertDataOption=insert_data_option, body=value).execute()
    values = result.get('updates', [])

    if not values:
        print('No data found.')
    else:
        print('Update Success')

if __name__ == '__main__':
    main()

