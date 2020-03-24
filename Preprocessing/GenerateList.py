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
    if faces.shape[0] != 1:
        facesAlt = faceCascadeAlt.detectMultiScale(imageCV2, haar_scale, min_neighbors, haar_flags, min_size)
        # Handle more failure
        if facesAlt.shape[0] != 1:
            facesTree = faceCascadeTree.detectMultiScale(imageCV2, haar_scale, min_neighbors, haar_flags, min_size)
            # Handle even more failure
            if facesTree.shape[0] != 1:
                raise Exception("Could not properly detect face for image")
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
    # Crop
    img = faceCrop(img)
    # Resize
    img.thumbnail((256,256), Image.ANTIALIAS)
    
    # cv2.imshow('Resized', pil2cv(img))
    # cv2.waitKey(0)

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
            

dbRoot = r'C:\Users\Will\Documents\Cohn-Kanade Database\Cohn-Kanade Database\CK+\cohn-kanade-images'
destRoot = r'C:\Users\Will\Documents\StoicNetData'

NO_REDO = True

if not os.path.exists(destRoot):
    os.makedirs(destRoot)

imagePairs = []
pairCount = 0
with os.scandir(dbRoot) as subjectEntries:
    subjectEntrys = list(subjectEntries)
    subjectCount = len(subjectEntrys)
    for subIndex in range(subjectCount):
        subjectEntry = subjectEntrys[subIndex]
        if subjectEntry.is_dir():
            print(subjectEntry.name)
            with os.scandir(dbRoot+ "\\" + subjectEntry.name) as sessionEntries:
                for sessionEntry in sessionEntries:
                    if sessionEntry.is_dir():
                        print("  |--" + sessionEntry.name)

                        imageEntries = os.listdir(dbRoot+"\\"+ subjectEntry.name +"\\"+  sessionEntry.name)
                        for imageEntry in imageEntries:
                            if imageEntry.endswith('.png'):
                                print("       |--" + imageEntry, end=' ')

                                if not os.path.exists(destRoot +"\\"+ subjectEntry.name +"\\"+ sessionEntry.name):
                                    os.makedirs(destRoot +"\\"+ subjectEntry.name +"\\"+ sessionEntry.name)

                                if NO_REDO and not os.path.exists(destRoot +"\\"+ subjectEntry.name +"\\"+ sessionEntry.name + "\\" + imageEntry):
                                    fixImage(
                                        dbRoot +"\\"+ subjectEntry.name +"\\"+ sessionEntry.name + "\\" + imageEntry,
                                        destRoot +"\\"+ subjectEntry.name +"\\"+ sessionEntry.name + "\\" + imageEntry
                                    )

                                randomOther = getRandomImg(subIndex)
                                print(' x  ' + randomOther)

                                imagePairs.append(
                                    (
                                        subjectEntry.name +"\\"+ sessionEntry.name + "\\" + imageEntries[0],
                                        subjectEntry.name +"\\"+ sessionEntry.name + "\\" + imageEntry,
                                        randomOther
                                    )
                                )
                                pairCount += 1


print(str(pairCount) + ' triplets/pairs')

# Write pair list to file
with open(destRoot + '\\pairs.txt', 'w') as fp:
    fp.write('\n'.join('{0}\t{1}'.format(ip[0],ip[1]) for ip in imagePairs))

# Write triplets list to file
with open(destRoot + '\\triplets.txt', 'w') as fp:
    fp.write('\n'.join('{0}\t{1}\t{2}'.format(ip[0],ip[1], ip[2]) for ip in imagePairs))
