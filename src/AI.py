import train
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
    #for key in patchMap:
        #print(str(key) + " : " + str(patchMap[key]))
    keys = [key for key in patchMap]
    return keys, patchMap

def basicAgent(image):
    k = 5
    im_width, im_height = image.size
    # k is number of clusters, 3rd argument is number of rounds of clustering 
    repColors = train.colorCluster(image, k, 5)
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
                patchDistances = [-1 for j in range(len(patchCenters))]
                # Get 1000 patch subsample to compare queried patch to
                patchCenters, patchMap = getPatchSubsample(grayIm, im_width, im_height)
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
    basicAgent(Image.open(dogePath))