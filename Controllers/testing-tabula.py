import os
from tabula import read_pdf
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import numpy as np

current_dir = os.getcwd()

# OCR improvement - Image processing
def preprocessing(pdf):

    # converting pdf to image
    image = convert_from_path(pdf, 500, poppler_path=r'C:\Program Files\poppler-22.11.0\Library\bin')[0]
    #newimg = pages.resize((pages.size[0]*2, pages.size[1]*2), Image.ANTIALIAS) didn't work

    # Sharping character borders from pages
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)

    # Increasing contrast from pages
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Reducing noise from pages
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(0.5)

    # Reducing image size -- Testing purpose
    image = image.resize((image.size[0]//2, image.size[1]//2), Image.ANTIALIAS)

    # save the image as pdf
    image.save(f'{current_dir}\\..\\Models\\trated.pdf', 'PDF', resolution=100.0, quality=20)


# preprocessing('fdp2.pdf')

# Actually working before preprocessing

df = read_pdf(f'{current_dir}\\..\\Models\\fdp2.pdf', pages=1, encoding='utf-8', multiple_tables=False)
print("Liste des etudiants \n")

df[0]["Emargement"] = df[0]["Emargement"].replace(r'\D+', 'present', regex=True)
df[0]["Emargement"] = df[0]["Emargement"].replace(np.nan, 'absent', regex=True)

print(df[0])
