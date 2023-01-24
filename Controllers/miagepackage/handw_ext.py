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
    file_name = response.full_text_annotation.text
    
    # ----------------- Data cleaning -----------------

    # file_name = "Nom : BOURGEOIS\nPrénom : Théo\nUE ou ECUE : MIAGE\nDate : 14/01/2021\nSalle : 357"

    file_name = file_name.replace("\n", " ")
    file_name = file_name.replace("/", "_")

    file_name = file_name.split(" ")
    # for all the elements in the list, delete all ":" and "Nom", "Prénom", "UE ou ECUE", "Date", "Salle"
    for i in range(len(file_name)):
        file_name[i] = file_name[i].replace(":", "")
        file_name[i] = file_name[i].replace("Nom", "")
        file_name[i] = file_name[i].replace("Prénom", "")
        file_name[i] = file_name[i].replace("UE", "")
        file_name[i] = file_name[i].replace("ou", "")
        file_name[i] = file_name[i].replace("EC", "")
        file_name[i] = file_name[i].replace("Date", "")
        file_name[i] = file_name[i].replace("Salle", "")
        
    # delete all the empty elements in the list
    file_name = list(filter(None, file_name))

    #create a string with all the elements of the list separated by a "_"
    file_name = "_".join(file_name)
    return file_name