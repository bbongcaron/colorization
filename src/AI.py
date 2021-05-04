import train
from math import exp
from PIL import Image, ImageOps
from random import randrange
import numpy as np
import os

def getPatchSubsample(grayIm, im_width, im_height):
    patchMap = {}
    for i in range(1000):
        randPixel = (randrange(1, im_height - 1), randrange(1, im_width // 2))
        patchMap[randPixel] = []
        for x in range(-1,2):
            for y in range(-1,2):
                patchMap[randPixel].append(grayIm[randPixel[0]+x][randPixel[1]+y])
    keys = [key for key in patchMap]
    return keys, patchMap

def advancedAgent(image):
    im_width, im_height = image.size
    wR, wG, wB = train.weightFitting(image)
    grayIm = np.array(ImageOps.grayscale(image))
    coloredIm = clusterColors = np.zeros((im_height,im_width,3), dtype=np.uint8)
    for u in range(1, im_height - 1):
        for v in range(1, im_width - 1):
            gray = [1]
            for x in range(-1,2):
                for y in range(-1,2):
                    gray.append(grayIm[u+x][v+y]/255)
            Rx = sum([wR[i]*gray[i] for i in range(len(wR))])
            Gx = sum([wG[i]*gray[i] for i in range(len(wG))])
            Bx = sum([wB[i]*gray[i] for i in range(len(wB))])
            predR = 255.0 / (1 + exp(-1 * Rx))
            predG = 255.0 / (1 + exp(-1 * Gx))
            predB = 255.0 / (1 + exp(-1 * Bx))
            coloredIm[u][v] = [predR, predG, predB]
    # Pathing and Saving
    finalImage = Image.fromarray(coloredIm)
    coloredImPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/images/advanced.jpg'
    finalImage.show()
    finalImage.save(coloredImPath)

def basicAgent(image):
    k = 5
    im_width, im_height = image.size
    # k is number of clusters, 3rd argument is number of rounds of clustering 
    repColors = train.colorCluster(image, k, 10)
    rgbIm = np.array(image)
    grayIm = np.array(ImageOps.grayscale(image))
    fiveColoredIm = clusterColors = np.zeros((im_height,im_width,3), dtype=np.uint8)
    # fiveColoredIm and grayIm => gray scale, but in RGB triplets
    for u in range(im_height):
        for v in range(im_width):
            fiveColoredIm[u][v] = [grayIm[u][v], grayIm[u][v], grayIm[u][v]]

    print('\tReplacing left half pixels with best representative colors...')
    for u in range(im_height):
        for v in range(im_width // 2):
            distToRepColors = [-1 for j in range(k)]
            # Find most similar representative color for that pixel
            for s in range(k):
                distToRepColors[s] = np.linalg.norm(rgbIm[u][v] - repColors[s])
            fiveColoredIm[u][v] = repColors[distToRepColors.index(min(distToRepColors))]
    print('\tDone!')
    
    for u in range(im_height):
        for v in range(im_width // 2, im_width):
            print('\tColoring Pixel ({:^5s},{:^5s}) with Basic Strategy...'.format(str(v), str(u)), end='\r')
            # Any edge cases will be colored black
            if u == im_height - 1 or u == 0 or v == im_width // 2 or v == im_width - 1:
                fiveColoredIm[u][v] = [0, 0, 0]
            else:
                queriedPatch = []
                # Get the 3x3 patch whose center pixel will be filled
                for x in range(-1,2):
                    for y in range(-1,2):
                        queriedPatch.append(grayIm[u + x][v + y])
                # Get 1000 patch subsample to compare queried patch to
                patchCenters, patchMap = getPatchSubsample(grayIm, im_width, im_height)
                patchDistances = [-1 for j in range(len(patchCenters))]
                # Find most similar grayscale patches
                for s in range(len(patchCenters)):
                    patchDistances[s] = np.linalg.norm(np.array(queriedPatch) - np.array(patchMap[patchCenters[s]]))
                mostSimilarPixel = patchCenters[patchDistances.index(min(patchDistances))]
                fiveColoredIm[u][v] = fiveColoredIm[mostSimilarPixel[0]][mostSimilarPixel[1]]

    # Pathing and saving
    grayImPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/images/grayImage.jpg'
    fiveColoredImPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/images/basic.jpg'
    Image.fromarray(grayIm).save(grayImPath)
    Image.fromarray(fiveColoredIm).save(fiveColoredImPath)

if __name__ == '__main__':
    dogePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/images/smolDoge.jpg'
    #basicAgent(Image.open(dogePath))
    advancedAgent(Image.open(dogePath))