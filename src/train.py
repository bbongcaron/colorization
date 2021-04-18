from PIL import Image
import numpy as np
import os

def colorCluster(image):
    im_width, im_height = image.size
    # in matrix, the format is rgbMatrix[y_coord, x_coord, r|g|b]
    rgbMatrix = np.array(image)
    print(rgbMatrix)
    for i in range(100):
        rgbMatrix[i,0:50] = [0,0,0]

    newDogePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/newDoge.jpg'
    image2 = Image.fromarray(rgbMatrix).save(newDogePath)
    return image2

if __name__ == '__main__':
    dogePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/doge.jpg'
    colorCluster(Image.open(dogePath))