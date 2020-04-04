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

    min_size = (150,150)
    haar_scale = 1.1
    min_neighbors = 3
    haar_flags = 0
    border_size = 50

    # Detect the faces
    imageCV2 = cv2.equalizeHist(imageCV)
    faces = faceCascade.detectMultiScale(imageCV2, haar_scale, min_neighbors, haar_flags, min_size)

    
    # Handling failure (mostly false positives)
    if (not faces.any()) or faces.shape[0] != 1:
        facesAlt = faceCascadeAlt.detectMultiScale(imageCV2, haar_scale, min_neighbors, haar_flags, min_size)
        # Handle more failure
        if (not facesAlt.any()) or facesAlt.shape[0] != 1:
            facesTree = faceCascadeTree.detectMultiScale(imageCV2, haar_scale, min_neighbors, haar_flags, min_size)
            # Handle even more failure
            if (not facesTree.any()) or facesTree.shape[0] != 1:
                faces = faceCascade.detectMultiScale(imageCV2)
                if not faces.any():
                    raise Exception("Could not properly detect face for image")
                else:
                    faces = faces[0]
            else:
                faces = facesTree
        else:
            faces = facesAlt

    # TODO: Comment this out for final run
    for ((x, y, w, h)) in faces:
        p1 = (x,y)
        p2 = (x+w, y+h)
        imageCVRect = cv2.rectangle(imageCV, p1, p2, (255,255,255), 5)

    ((x, y, w, h)) = faces[0]
    x = max(x - border_size, 0)
    y = max(y - border_size, 0)
    w = w + 2*border_size
    h = h + 2*border_size

    # cv2.imshow('To-crop', imageCVRect)

    original = pil2cv(image)
    imageCropCV = original[y:y+h, x:x+w]
    
    # cv2.imshow('Cropped', imageCropCV)

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
    
    cv2.imshow('Resized', pil2cv(img))
    cv2.waitKey(0)
    
    # Crop
    img = faceCrop(img)
    
    cv2.imshow('Resized', pil2cv(img))
    cv2.waitKey(0)
    
    # Resize
    img.thumbnail((256,256), Image.ANTIALIAS)
    
    cv2.imshow('Resized', pil2cv(img))
    cv2.waitKey(0)

    img.save(toPath)

def getRandomImg(subjectIndex):
    ri = random.randint(0,subjectCount-2) # -1 for proper indexing, -1 to skip current index
    if ri >= subIndex:
        ri += 1 # skip over the current index
    subjectEntry = subjectEntrys[ri].name

    with os.scandir(dbRoot+ "\\" + subjectEntry) as sessionEntries:
        sessionEntrys = list(sessionEntries)
        ri = random.randint(0,len(sessionEntrys)-1)
        sessionEntry = sessionEntrys[ri]
        if sessionEntry.is_dir():
            imageEntries = os.listdir(dbRoot+"\\"+ subjectEntry +"\\"+  sessionEntry.name)
            ri = random.randint(0,len(imageEntries)-1)
            imageEntry = imageEntries[ri]
            if imageEntry.endswith('.png'):
                return subjectEntry +"\\"+ sessionEntry.name + "\\" + imageEntry
            else:
                print("D'OH!:" +dbRoot+"\\"+subjectEntry+"\\"+sessionEntry.name+"\\"+imageEntry)
                input("PUSH ENTER TO EXTERMINATE IMPURITY AND CONTINUE")
                os.remove(dbRoot+"\\"+subjectEntry+"\\"+sessionEntry.name+"\\"+imageEntry)
                return getRandomImg(subjectIndex)
        else:
            print("D'OH!:" +dbRoot+"\\"+subjectEntry+"\\"+sessionEntry.name)
            input("PUSH ENTER TO EXTERMINATE IMPURITY AND CONTINUE")
            os.remove(dbRoot+"\\"+subjectEntry+"\\"+sessionEntry.name)
            return getRandomImg(subjectIndex)
            

dbRoot = r'C:\Users\Will\Documents\StoicNetData\Custom\inputs'
destRoot = r'C:\Users\Will\Documents\StoicNetData\Custom'

imageEntries = os.listdir(dbRoot)
counter = 1
for imageEntry in imageEntries:
    if imageEntry.endswith('.png') or imageEntry.endswith('.jpg'):
        print("|--" + imageEntry)
        
        fixImage(
            dbRoot +"\\"+ imageEntry,
            destRoot + "\\test{0}.png".format(counter)
        )
        counter += 1


