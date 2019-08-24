import json 

def parse_slide(slide_content):
    for line in slide_content.split('\n'):
        pass

    # Look up Markdown specs to see how they parse

def make_slide():
    pass

def main():
    filename = input('What .md file would you like to convert to Slides? ')

    markdown = open(filename, 'r').read
    slide_contents = markdown.split('!!slide')

    for slide_content in slide_contents:
        slide_json = parse_slide(slide_content)
        make_slide(slide_json)
