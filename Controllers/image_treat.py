import os
from pdf2image import convert_from_path
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

current_dir = os.getcwd()

def cheking_absences(file):
  
  if os.path.splitext(file)[1] == '.pdf':
    # convert pdf to image
    pages = convert_from_path(file, 500, poppler_path=r'C:\Program Files\poppler-22.11.0\Library\bin')
    # for page in pages:
    #     page.save('out.jpg', 'JPEG')
    pages[0].save(f'{current_dir}\\models\\out.jpg', 'JPEG')
  
  # ----------------- 1. Find the table in the image -----------------
  # Based on the code from https://stackoverflow.com/questions/55279305/extract-table-from-image-to-another-image-by-python-3

  img = cv2.imread(f'{current_dir}\\models\\out.jpg', cv2.IMREAD_COLOR)
  gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  _, thr = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
  close = cv2.morphologyEx(255 - thr, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
  contours, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  areaThr = 3000

  area = cv2.contourArea(contours[1])
  if (area > areaThr):
    x, y, width, height = cv2.boundingRect(contours[1])
    cv2.imwrite(f'{current_dir}\\models\\output.png', img[y:y+height-1, x:x+width-1])


  # ----------------- 2. Finding the table's countours -----------------

  im1 = cv2.imread(f'{current_dir}\\models\\output.png', 0)
  im = cv2.imread(f'{current_dir}\\models\\output.png')

  ret,thresh_value = cv2.threshold(im1,180,255,cv2.THRESH_BINARY_INV)

  kernel = np.ones((5,5),np.uint8)
  dilated_value = cv2.dilate(thresh_value,kernel,iterations = 1)

  contours, hierarchy = cv2.findContours(dilated_value,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

  cordinates = []
  for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    cordinates.append((x,y,w,h))
    #bounding the images
    if y< 50:
        continue

    cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),1)

  plt.imshow(im)
  #plt.show()
  cv2.namedWindow('detecttable', cv2.WINDOW_NORMAL)
  cv2.imwrite(f'{current_dir}\\models\\detecttable.jpg',im)

  # ----------------- 3. Are the cells empty or not -----------------

  # Say if the biggest contours are empty or not
  # clist = []
  # for cnt in contours:
  #   clist.append(cv2.contourArea(cnt))

  # print(f'37 :  {clist[37]} 38 :  {clist[38]} 39 :  {clist[39]}')
  # # print(max(clist))
  # my_dict = {i:clist.count(i) for i in clist}
  # print(my_dict.values())
  # filtered_dict = {k:v for (k,v) in my_dict.items() if k==2024.0 in k}
  # print(filtered_dict)



# cheking_absences(f'{current_dir}\\models\\out.jpg')
cheking_absences(f'{current_dir}\\models\\trated.pdf')