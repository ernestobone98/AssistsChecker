import os, io
from google.cloud import vision
import pandas as pd

current_dir = os.getcwd()
sep = os.sep

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{current_dir}{sep}controllers{sep}miagepackage{sep}application_default_credentials.json'
client = vision.ImageAnnotatorClient()

FOLDER_PATH = f'{current_dir}{sep}models{sep}'
IMG = 'fdp6.jpg'

FILE_PATH = FOLDER_PATH + IMG

with io.open(FILE_PATH, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)
response = client.document_text_detection(image=image)
document = response.full_text_annotation.text
print(document)