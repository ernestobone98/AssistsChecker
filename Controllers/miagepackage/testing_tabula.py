import os
from tabula import read_pdf
from tabula import read_pdf_with_template
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import numpy as np

current_dir = os.getcwd()
sep = os.path.sep

# OCR improvement - Image processing (Only works on Windows)
def preprocessing(file, image_name):

    if os.path.splitext(file)[1] == '.pdf':
        # converting pdf to image
        image = convert_from_path(file, 500, poppler_path=r'C:\Program Files\poppler-22.11.0\Library\bin')[0]
    #newimg = pages.resize((pages.size[0]*2, pages.size[1]*2), Image.ANTIALIAS) didn't work
    else:
        image = Image.open(file)
    # Converting image to grayscale
    image = image.convert('L')

    # Sharping character borders from pages
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)

    # Increasing contrast from pages
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Reducing noise from pages
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(0.5)

    # higher brightness on dark zones of the image
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.5)

    image = image.crop((0, 1200, 3860, 2000))

    # save the image as pdf
    image.save(f'{current_dir}{sep}Models{sep}{image_name}.jpg', 'JPEG')
    

preprocessing(f'{current_dir}{sep}Models{sep}fdp14.pdf', 'fdp14')

#  ------------- Main function Definition ----------------

def check_presence(file, json_file_name):

    df = read_pdf(f'{current_dir}{sep}Models{sep}{file}', pages="all", encoding='utf-8', multiple_tables=False)
    print("---------- DEBUG ---------- 1st file \n")

    df[0]["Emargement"] = df[0]["Emargement"].replace(r'.+', 'present', regex=True)
    df[0]["Emargement"] = df[0]["Emargement"].replace(np.nan, 'absent', regex=True)
    df[0] = df[0].drop(columns=['Prénom'])
    df[0].rename(columns={df[0].columns[0]: 'Civilité', df[0].columns[1]: 'Nom patronymique', df[0].columns[2]: 'Prénom', df[0].columns[3]: 'Émargement'}, inplace=True)

    # df[0].to_csv(f'{current_dir}{sep}Models{sep}test.csv', index=False)
    df[0].to_json(f'{current_dir}{sep}Models{sep}{json_file_name}.json', orient='records')

