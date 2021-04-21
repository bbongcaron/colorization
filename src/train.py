from PIL import Image
from random import randrange
import numpy as np
import os

def colorCluster(image):
    im_width, im_height = image.size
    rgbMatrix = np.array(image)
    #print(rgbMatrix)
    #for i in range(100):
    #    rgbMatrix[i,0:50] = [0,0,0]
    # (0,0) is top left corner of image, (0, width) is top right corner of image
    k = 5
    centers = [[rgbMatrix[randrange(im_height)][randrange(im_width)],rgbMatrix[randrange(im_height)][randrange(im_width)], rgbMatrix[randrange(im_height)][randrange(im_width)]] for i in range(k)]
    clusters = None
    tmax = 5
    for i in range(tmax):
        print('{:100s}'.format('Clustering Round #' + str(i) + ':'))
        clusters = [[] for i in range(k)]
        for u in range(im_height):
            for v in range(im_width):
                print('\tCalculating Center Distances for Pixel ({:^5s},{:^5s})'.format(str(v), str(u)), end='\r')
                distToCenters = [-1 for j in range(k)]
                for s in range(k):
                    distToCenters[s] = np.linalg.norm(rgbMatrix[u][v] - centers[s])
                bestClusterIndex = distToCenters.index(min(distToCenters))
                clusters[bestClusterIndex].append(rgbMatrix[u][v])
        for s in range(k):
            sumVects = np.array([0,0,0])
            for vector in clusters[s]:
                sumVects = sumVects + np.array(vector)
            centers[s] = sumVects // np.linalg.norm(clusters[s])
        print('{:100s}'.format('Done!'))
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
    clusterColorsPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/clusterColors.jpg'
    Image.fromarray(clusterColors).save(clusterColorsPath)
    print(centers)

    #newDogePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/newDoge.jpg'
    #image2 = Image.fromarray(rgbMatrix).save(newDogePath)
    return

if __name__ == '__main__':
    dogePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/doge.jpg'
    colorCluster(Image.open(dogePath))