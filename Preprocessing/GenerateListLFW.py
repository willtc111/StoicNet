import os
import sys
import cv2
import numpy as np
import random
from PIL import Image
from time import sleep

# The face detectors
faceCascade = cv2.CascadeClassifier(r'C:\OpenCV-3.4.5\opencv\build\etc\haarcascades\haarcascade_frontalface_default.xml')
faceCascadeAlt = cv2.CascadeClassifier(r'C:\OpenCV-3.4.5\opencv\build\etc\haarcascades\haarcascade_frontalface_alt.xml')
faceCascadeTree = cv2.CascadeClassifier(r'C:\OpenCV-3.4.5\opencv\build\etc\haarcascades\haarcascade_frontalface_alt_tree.xml')


def faceCrop(image):
    imageCV = pil2cv(image)

    border_size = 25
    sf = 1.1
    mn = 3
    ms = (90,90)
    
    # Detect the faces
    imageCV2 = cv2.equalizeHist(imageCV)
    faces = faceCascade.detectMultiScale(imageCV2, scaleFactor=sf, minNeighbors=mn, minSize=ms)
    # Handling failure (mostly false positives)
    if len(faces) != 1 or faces.shape[0] != 1:
        facesAlt = faceCascadeAlt.detectMultiScale(imageCV2, scaleFactor=sf, minNeighbors=mn, minSize=ms)
        # Handle more failure
        if len(facesAlt) != 1 or facesAlt.shape[0] != 1:
            facesTree = faceCascadeTree.detectMultiScale(imageCV2, scaleFactor=sf, minNeighbors=mn, minSize=ms)
            # Handle even more failure
            if len(facesTree) != 1 or facesTree.shape[0] != 1:
                faces = faceCascadeTree.detectMultiScale(imageCV2, minSize=ms)
                if len(faces) < 1 or faces.shape[0] < 1:
                    raise Exception("Could not properly detect face for image")
                else:
                    # Take the largest face
                    bestFace = [0,0,0,0]
                    for face in faces:
                        if face[3] > bestFace[3]:
                            bestFace = face
                    faces = [bestFace]
            else:
                faces = facesTree
        else:
            faces = facesAlt

    #print('"{}"'.format(faces))

    # TODO: Comment this out for final run
    for ((x, y, w, h)) in faces:
        p1 = (x,y)
        p2 = (x+w, y+h)
        imageCVRect = cv2.rectangle(imageCV, p1, p2, (255,255,255), 3)
        
        #cv2.imshow('To-crop', imageCVRect)
        #cv2.waitKey(0)

    ((x, y, w, h)) = faces[0]
    x = max(x - border_size, 0)
    y = max(y - border_size, 0)
    w = w + 2*border_size
    h = h + 2*border_size


    original = pil2cv(image)
    imageCropCV = original[y:y+h, x:x+w]
    
    #cv2.imshow('Cropped', imageCropCV)
    #cv2.waitKey(0)

    imageCropPIL = cv2pil(imageCropCV)
    return imageCropPIL


def pil2cv(pil_im):
    pil_im = pil_im.convert('L')
    cv_im = np.array(pil_im)
    return cv_im


def cv2pil(cv_im):
    return Image.fromarray(cv_im)


def fixImage(fromPath, toPath):
    img = Image.open(fromPath)
    # Crop
    img = faceCrop(img)
    # Resize
    img.thumbnail((256,256), Image.ANTIALIAS)
    
    # cv2.imshow('Resized', pil2cv(img))
    # cv2.waitKey(0)

    img.save(toPath)
            

dbRoot = r'C:\Users\Will\Documents\LFW Dataset\lfw_funneled'
destRoot = r'C:\Users\Will\Documents\StoicNetData\LFW'

NO_REDO = True

if not os.path.exists(destRoot):
    os.makedirs(destRoot)

imageList = []
oldCount = 0
newCount = 0
failCount = 0
print("LFW")
with os.scandir(dbRoot) as personEntries:
    personEntries = list(personEntries)
    personCount = len(personEntries)
    for personIndex in range(personCount):
        personEntry = personEntries[personIndex]
        if personEntry.is_dir():
            printedName = False
            imageEntries = os.listdir(dbRoot + "\\" + personEntry.name)
            for imageEntry in imageEntries:
                if imageEntry.endswith('.jpg'):
                    #print("   |--" + imageEntry, end='\t')

                    if NO_REDO and os.path.exists(destRoot + "\\" + personEntry.name + "\\" + imageEntry):
                        #print(" . ")    # skip!
                        oldCount += 1
                    else:
                        if not printedName:
                            print("|--" + personEntry.name)
                            printedName=True
                        print("   |--" + imageEntry, end='\t')
                        if not os.path.exists(destRoot + "\\" + personEntry.name):
                            os.makedirs(destRoot + "\\" + personEntry.name)
                        try:
                            fixImage(
                                dbRoot + "\\" + personEntry.name + "\\" + imageEntry,
                                destRoot + "\\" + personEntry.name + "\\" + imageEntry
                            )
                        except Exception as ex:
                            print(" -\t{0}".format(ex))
                            failCount += 1
                        else:
                            print(" + ")
                            imageList.append(personEntry.name +"\\"+ imageEntry)
                            newCount += 1

print(str(newCount) + ' new images')
print(str(oldCount) + ' old images')
print(str(failCount) + ' failures')

# Write pair list to file
with open(destRoot + '\\images.txt', 'w') as fp:
    fp.write('\n'.join('{0}'.format(ip) for ip in imageList))

