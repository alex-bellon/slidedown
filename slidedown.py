from __future__ import print_function
import pickle, json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/presentations']

# The ID of a sample presentation.
PRESENTATION_ID = '1EAYk18WDjIG-zp_0vLm3CsfQh_i8eXc67Jo2O9C6Vuc'

def auth():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token: creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token: pickle.dump(creds, token)

    return creds

def make_slides(creds, slide_dict):
    service = build('slides', 'v1', credentials=creds)
    body = { 'title': slide_dict['title'] }
    print(body)
    presentation = service.presentations().create(body=body).execute()
    print('Created presentation with ID: {0}'.format(presentation.get('presentationId')))

def parse_slide(slide_content):
    result = dict()
    slide_content.replace('\r\n', '\n')
    for line in slide_content.split('\n'):
        if line[:2] == '# ':
            result['title'] = line[2:]
    # Look up Markdown specs to see how they parse
    print(result)
    return result

def main():
    filename = input('What .md file would you like to convert to Slides? ')

    markdown = open(filename, 'r').read()
    slide_contents = markdown.split('$slide')

    creds = auth()
    for slide_content in slide_contents:
        slide_dict = parse_slide(slide_content)
        if slide_dict: make_slides(creds, slide_dict)

main()
