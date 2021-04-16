import os
import cv2

def loadIds():
    path = r'.\id'
    print("success")
    files = os.listdir(path)
    Ids = []
    for file in files:
        extension = os.path.splitext(file)
        if extension[1] in ['.jpg','.png','.jpeg']:
            img = cv2.imread(os.path.join(path,file))
            img_resized = cv2.resize(img,(500,500))
            Ids.append(img_resized)
    return Ids