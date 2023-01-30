import os, io
from google.cloud import vision

current_dir = os.getcwd()
sep = os.sep
FOLDER_PATH = f'{current_dir}{sep}models{sep}'

def get_header(img):

    # Using Google Vision API, we can extract handwritten text from the image

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{current_dir}{sep}controllers{sep}miagepackage{sep}application_default_credentials.json'
    client = vision.ImageAnnotatorClient()

    IMG = img

    FILE_PATH = FOLDER_PATH + IMG

    with io.open(FILE_PATH, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation.text

    return document

def trating_text(img):

    Global_name = "Archive des FDP"     # Name of the folder where the pdf will be stored

    # ---------------------- Extracting Promotion and Group from the pdf name ----------------------

    file_name = get_header(img)

    # ------------- cleaning the file_name variable -------------
    a_retirer = ["Nom:", "Nom :", "Prénom:", "Prénom :", "UE ou ECUE:", "UE ou ECUE :", "Date:", "Date :", "Salle:", "Salle :","«", "»", "<<", ">>"]
    for e in a_retirer:
        file_name = file_name.replace(e,"")

    lignes = file_name.split("\n")
    lignes = [l for l in lignes if l != '']
    lignes = [ligne.strip(" ") for ligne in lignes]
        
    lignes = list(filter(None, lignes))

    classe_name =  lignes[0] # EX : "CM-M1 MIAGE"
    promo_name =  lignes[1].replace("/", "_") # EX : "PROMOTION Marvin Lee Minski 2021/2024"
    lignes[1] = promo_name
    prof_name = lignes[2] + " " + lignes[3] # EX : "Donati Leo"
    lignes[2] = prof_name
    UE_ECUE_name = lignes[4] # Ex : "TERD"
    lignes[5] = lignes[5].replace("/", "_") + "_" + lignes[6] # Ex : "10_01_23_TD7"
    lignes.pop(3)
    lignes.pop(5)
    lignes.insert(0, Global_name)

    # ------------------- Folders creation : Gobal_name/classe_name/promo_name/prof_name/UE_ECUE_name/DATE_salle_name -------------------

    if not os.path.exists(Global_name):
        os.makedirs(Global_name)
    os.chdir(Global_name)


    if not os.path.exists(classe_name):
        os.makedirs(classe_name)
    os.chdir(classe_name)


    if not os.path.exists(promo_name):
        os.makedirs(promo_name)
    os.chdir(promo_name)


    if not os.path.exists(prof_name):
        os.makedirs(prof_name)
    os.chdir(prof_name)


    if not os.path.exists(UE_ECUE_name):
        os.makedirs(UE_ECUE_name)
    os.chdir(UE_ECUE_name)
    os.chdir(current_dir)

    return lignes