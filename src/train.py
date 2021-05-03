from PIL import Image, ImageOps
from random import randrange
from math import exp
import time
import numpy as np
import os

def weightFitting(image):
    im_width, im_height = image.size
    rgbMatrix = np.array(image)
    grayIm = np.array(ImageOps.grayscale(image))
    alpha = 0.0001
    wR = [0.5 for i in range(10)]
    wG = [0.5 for i in range(10)]
    wB = [0.5 for i in range(10)]
    start = time.time()
    for s in range(150000):
        print("Round {:7s}".format(str(s+1)), end='\r')
        randPixel = (randrange(1, im_height - 1), randrange(1, im_width // 2))
        r = rgbMatrix[randPixel[0]][randPixel[1]][0]
        g = rgbMatrix[randPixel[0]][randPixel[1]][1]
        b = rgbMatrix[randPixel[0]][randPixel[1]][2]
        gray = [1]
        for x in range(-1,2):
            for y in range(-1,2):
                gray.append(grayIm[randPixel[0]+x][randPixel[1]+y]/255)

        Rx = sum([wR[i]*gray[i] for i in range(len(wR))])
        Gx = sum([wG[i]*gray[i] for i in range(len(wG))])
        Bx = sum([wB[i]*gray[i] for i in range(len(wB))])

        predR = 255.0 / (1 + exp(-1 * Rx))
        predG = 255.0 / (1 + exp(-1 * Gx))
        predB = 255.0 / (1 + exp(-1 * Bx))

        gLossR = [(predR - r)*predR*(1 - predR/255.0)*gray[i] for i in range(len(gray))]
        gLossG = [(predG - g)*predG*(1 - predG/255.0)*gray[i] for i in range(len(gray))]
        gLossB = [(predB - b)*predB*(1 - predB/255.0)*gray[i] for i in range(len(gray))]

        wR = [wR[i] - alpha*gLossR[i] for i in range(len(wR))]
        wG = [wG[i] - alpha*gLossG[i] for i in range(len(wG))]
        wB = [wB[i] - alpha*gLossB[i] for i in range(len(wB))]

    end = time.time()
    print("Elapsed Time: " + str(end - start) + "s")
    return wR, wG, wB

def colorCluster(image, k, numRounds):
    im_width, im_height = image.size
    image.show()
    rgbMatrix = np.array(image)
    #print(rgbMatrix)
    #for i in range(100):
    #    rgbMatrix[i,0:50] = [0,0,0]
    # (0,0) is top left corner of image, (0, width) is top right corner of image
    centers = [[rgbMatrix[randrange(im_height)][randrange(im_width)],rgbMatrix[randrange(im_height)][randrange(im_width)], rgbMatrix[randrange(im_height)][randrange(im_width)]] for i in range(k)]
    for center in centers:
        print(center)
    clusters = None
    for i in range(numRounds):
        print('{:100s}'.format('Clustering Round #' + str(i+1) + ':'))
        clusters = [[] for i in range(k)]
        for u in range(im_height):
            for v in range(im_width):
                print('\tCalculating Center Distances for Pixel ({:^5s},{:^5s})'.format(str(v), str(u)), end='\r')
                distToCenters = [None for j in range(k)]
                for s in range(k):
                    distToCenters[s] = np.linalg.norm(np.array(centers[s]) - rgbMatrix[u][v])
                bestClusterIndex = distToCenters.index(min(distToCenters))
                clusters[bestClusterIndex].append(rgbMatrix[u][v])
        for s in range(k):
            sumVects = np.array([0,0,0])
            for vector in clusters[s]:
                sumVects = sumVects + np.array(vector)
            denom = len(clusters[s])
            if denom == 0:
                centers[s] = [0,0,0]
            else:
                centers[s] = sumVects // denom
        print('{:100s}'.format('Done!'))
        for center in centers:
            print(center)
    clusterColors = np.zeros((125,125,3), dtype=np.uint8)
    for i in range(125):
        for j in range(125):
            if i < 25:
                clusterColors[i][j] = centers[0]
            elif i < 50:
                clusterColors[i][j] = centers[1]
            elif i < 75:
                clusterColors[i][j] = centers[2]
            elif i < 100:
                clusterColors[i][j] = centers[3]
            elif i < 125:
                clusterColors[i][j] = centers[4]
    clusterColorsPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/images/clusterColors.jpg'
    Image.fromarray(clusterColors).save(clusterColorsPath)
    return centers
