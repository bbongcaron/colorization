from PIL import Image
from random import randrange
from math import exp
import numpy as np
import os

def weightFitting(image):
    im_width, im_height = image.size
    rgbMatrix = np.array(image)
    grayIm = np.array(ImageOps.grayscale(image))
    alpha = 0.1
    # Models
    # r(g) = 255 / (1 + e^[-(w0 + w1*g1 + w2*g2 + w3*g3 + w4*g4 + w5*g5 + w6*g6 + w7*g7 + w8*g8 + w9*g9)])
    wR = [0.5 for i in range(10)]
    wG = [0.5 for i in range(10)]
    wB = [0.5 for i in range(10)]
    for i in range(10):
        randPixel = (randrange(1, im_height - 1), randrange(1, im_width // 2))
        r = rgbMatrix[randPixel[0]][randPixel[1]][0]
        g = rgbMatrix[randPixel[0]][randPixel[1]][1]
        b = rgbMatrix[randPixel[0]][randPixel[1]][2]
        gray = [1]
        for x in range(-1,2):
            for y in range(-1,2):
                gray.append(grayIm[randPixel[0]+x][randPixel[1]+y])
        Rx = wR[0]*gray[0] + wR[1]*gray[1] + wR[2]*gray[2] + wR[3]*gray[3] + wR[4]*gray[4] + wR[5]*gray[5] + wR[6]*gray[6] + wR[7]*gray[7] + wR[8]*gray[8] + wR[9]*gray[9]
        Gx = wG[0]*gray[0] + wG[1]*gray[1] + wG[2]*gray[2] + wG[3]*gray[3] + wG[4]*gray[4] + wG[5]*gray[5] + wG[6]*gray[6] + wG[7]*gray[7] + wG[8]*gray[8] + wG[9]*gray[9]
        Bx = wG[0]*gray[0] + wB[1]*gray[1] + wB[2]*gray[2] + wB[3]*gray[3] + wB[4]*gray[4] + wB[5]*gray[5] + wB[6]*gray[6] + wB[7]*gray[7] + wB[8]*gray[8] + wB[9]*gray[9]
        predR = 255 / (1 + exp(-1 * Rx))
        predG = 255 / (1 + exp(-1 * Gx))
        predB = 255 / (1 + exp(-1 * Bx))
        
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

if __name__ == '__main__':
    #dogePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/images/doge.jpg'
    #colorCluster(Image.open(dogePath))
    #arr = np.array([2, 4, 6])
    #print(arr/2)
    print(e)