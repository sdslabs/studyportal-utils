from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# from colors import blue, bold

ROOT = os.path.dirname(os.path.abspath(__file__))
TOKEN_PICKLE = os.path.join(ROOT, 'token.pickle')
CREDENTIALS = os.path.join(ROOT, 'credentials.json')


def driveinit():
    creds = None
    SCOPES = [
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive.appdata',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email',
        'openid',
    ]
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS,
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)

    user_service = build('oauth2', 'v2', credentials=creds)
    info = user_service.userinfo().get().execute()
    print(
        "Accessing drive of user {} <{}>"
        .format(((info['name'])), info['email'])
    )

    return service


if __name__ == '__main__':
    driveinit()
