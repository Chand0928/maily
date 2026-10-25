"""
gmail_tools.py - Handles Gmail API authentication, email reading, and draft creation.
"""

import os
import base64
import re
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API Scopes:
# - gmail.readonly: Read emails without modify/delete permissions
# - gmail.compose: Create drafts without ability to send
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose'
]


def authenticate_gmail(credentials_path: str = 'credentials.json', token_path: str = 'token.json'):
    """
    Authenticates with the Gmail API via OAuth2.
    Loads existing token or prompts login via browser on first run.
    """
    creds = None
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception:
            creds = None

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"'{credentials_path}' not found!\n"
                    "Please download your OAuth client credentials from Google Cloud Console "
                    f"and place them in the project folder as '{credentials_path}'."
                )

            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for the next run
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def _extract_body_from_payload(payload: dict) -> str:
    """
    Recursively extracts plain text (or cleaned HTML) body from a Gmail message payload.
    """
    body_text = ""

    # Case 1: Simple payload with body data
    if 'body' in payload and payload['body'].get('data'):
        data = payload['body']['data']
        decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
        mime_type = payload.get('mimeType', '')
        if 'text/plain' in mime_type:
            return decoded
        elif 'text/html' in mime_type:
            # Strip html tags
            return re.sub(r'<[^>]+>', ' ', decoded)

    # Case 2: Multipart payload
    parts = payload.get('parts', [])
    plain_parts = []
    html_parts = []

    def walk_parts(part_list):
        for part in part_list:
            mime = part.get('mimeType', '')
            if mime == 'text/plain' and part.get('body', {}).get('data'):
                decoded = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='replace')
                plain_parts.append(decoded)
            elif mime == 'text/html' and part.get('body', {}).get('data'):
                decoded = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='replace')
                clean_html = re.sub(r'<[^>]+>', ' ', decoded)
                html_parts.append(clean_html)
            elif 'parts' in part:
                walk_parts(part['parts'])

    walk_parts(parts)

    if plain_parts:
        body_text = "\n".join(plain_parts)
    elif html_parts:
        body_text = "\n".join(html_parts)

    # Clean multiple spaces and newlines
    body_text = re.sub(r'\n\s*\n+', '\n\n', body_text).strip()
    return body_text


def get_unread_emails(service, max_results: int = 5, query: str = 'is:unread'):
    """
    Fetches unread emails matching the search query.
    Returns a list of parsed email dictionaries.
    """
    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])
    parsed_emails = []

    for msg_meta in messages:
        msg_id = msg_meta['id']
        msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        
        payload = msg.get('payload', {})
        headers_list = payload.get('headers', [])
        
        headers = {h['name'].lower(): h['value'] for h in headers_list}
        
        from_hdr = headers.get('from', 'Unknown Sender')
        to_hdr = headers.get('to', '')
        subject_hdr = headers.get('subject', '(No Subject)')
        date_hdr = headers.get('date', '')
        message_id_hdr = headers.get('message-id', '')

        snippet = msg.get('snippet', '')
        body = _extract_body_from_payload(payload)
        
        # Fallback to snippet if body extraction was empty
        if not body or len(body.strip()) == 0:
            body = snippet

        parsed_emails.append({
            'id': msg['id'],
            'threadId': msg.get('threadId', msg['id']),
            'from': from_hdr,
            'to': to_hdr,
            'subject': subject_hdr,
            'date': date_hdr,
            'message_id': message_id_hdr,
            'snippet': snippet,
            'body': body
        })

    return parsed_emails


def create_draft_reply(service, original_email: dict, reply_text: str):
    """
    Creates a draft reply attached to the original email thread.
    Does NOT send the email.
    """
    message = EmailMessage()
    message.set_content(reply_text)

    # Set recipient as original sender
    message['To'] = original_email['from']

    # Set subject with Re: prefix if not present
    original_subject = original_email.get('subject', '')
    if original_subject.lower().startswith('re:'):
        message['Subject'] = original_subject
    else:
        message['Subject'] = f"Re: {original_subject}"

    # Set threading headers to link reply to conversation thread
    if original_email.get('message_id'):
        message['In-Reply-To'] = original_email['message_id']
        message['References'] = original_email['message_id']

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    draft_body = {
        'message': {
            'raw': encoded_message,
            'threadId': original_email['threadId']
        }
    }

    draft = service.users().drafts().create(
        userId='me',
        body=draft_body
    ).execute()

    return draft
