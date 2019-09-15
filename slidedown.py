from __future__ import print_function
import pickle, json, random
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

def make_presentation(creds, title):
    service = build('slides', 'v1', credentials=creds)
    body = {'title': title}
    presentation = service.presentations().create(body=body).execute()
    presentation_id = presentation.get('presentationId')
    return (service, presentation_id)

def parse_slide(slide_content, service_tuple, objectId):
    result = dict()
    slide_content.replace('\r\n', '\n')
    for line in slide_content.split('\n'):
        if line.replace('\n', ''):
            if line[:2] == '# ':
                result['title'] = line[2:]
                text_box('title', line, service_tuple, objectId) # need to make names unique
            text_box('test' + str(random.randint(10, 1000)), line, service_tuple, objectId)

    # Look up Markdown specs to see how they parse
    print(result)
    return result

def make_slide(service_tuple, objectId):
    requests = [
        {
            'createSlide': {
                'objectId': objectId,
                'insertionIndex': '1',
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                }
            }
        }
    ]
    # Execute the request.
    body = {'requests': requests}
    response = service_tuple[0].presentations().batchUpdate(presentationId=service_tuple[1], body=body).execute()
    create_slide_response = response.get('replies')[0].get('createSlide')
    print('Created slide with ID: {0}'.format(create_slide_response))

def text_box(name, content, service_tuple, objectId):
    element_id = name
    pt350 = {'magnitude': 350, 'unit': 'PT'}
    requests = [
        {
            'createShape': {
                'objectId': element_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': objectId,
                    'size': {'height': pt350, 'width': pt350},
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 350,
                        'translateY': 100,
                        'unit': 'PT'
                    }
                }
            }
        },

        {
            'insertText': {
                'objectId': element_id,
                'insertionIndex': 0,
                'text': content
            }
        }
    ]
    body = {'requests': requests}
    response = service_tuple[0].presentations().batchUpdate(presentationId=service_tuple[1], body=body).execute()

def main():
    filename = input('What .md file would you like to convert to Slides? ')
    markdown = open(filename, 'r').read()
    slide_contents = markdown.split('$slide')

    creds = auth()
    service_tuple = make_presentation(creds, filename[:-3])
    for slide_content in slide_contents:
        objectId = str(random.randint(10000, 100000))
        make_slide(service_tuple, objectId)
        slide_dict = parse_slide(slide_content, service_tuple, objectId)


main()
