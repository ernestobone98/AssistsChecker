import os, io
from google.cloud import vision
import pandas as pd


def get_header(img):

    current_dir = os.getcwd()
    sep = os.sep

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{current_dir}{sep}controllers{sep}miagepackage{sep}application_default_credentials.json'
    client = vision.ImageAnnotatorClient()

    FOLDER_PATH = f'{current_dir}{sep}models{sep}'
    IMG = img

    FILE_PATH = FOLDER_PATH + IMG

    with io.open(FILE_PATH, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation.text
    
    # where document = "Nom : BUFFA \nPrénom : Michel \nUE ou ECUE: Angular \nDate / salle : 22/01/2023 \nTD7"
    #we want to return file_name = "DONATI_Leo_Mathématiques_22_01_2023_357"
    file_name = document.split('\n')[0].split(':')[1].strip() + '_' + document.split('\n')[1].split(':')[1].strip() + '_' + document.split('\n')[2].split(':')[1].strip() + '_' + document.split('\n')[3].split(':')[1].strip().replace('/', '_') + '_' + document.split('\n')[4].strip()
    print (file_name)

get_header('fdp8.jpg')