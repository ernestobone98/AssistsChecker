import os, io
from google.cloud import vision

def get_header(img):

    current_dir = os.getcwd()
    sep = os.sep

    # Using Google Vision API, we can extract handwritten text from the image

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
    
    # where document is a string, i.e. document = "Nom : BUFFA \nPrénom : Michel \nUE ou ECUE: Angular \nDate / salle : 22/01/2023 \n357"
    # we want to return file_name = "Angular_BUFFA_Michel_22_01_2023_357"
    # we split the string into a list of strings, i.e. document = ["Nom : BUFFA ", "Prénom : Michel ", "UE ou ECUE: Angular ", "Date / salle : 22/01/2023 ", "357"]
    document = document.split("\n")
    # extract charracters after ": " in each string, i.e. document = ["BUFFA", "Michel", "Angular", "22/01/2023", "357"]
    document = [x.split(": ")[1] for x in document[:-1]]
    file_name = document[2] + "_" + document[0] + "_" + document[1] + "_" + document[3].replace("/", "_")
    #\n + "_" + document[4]
    return file_name
