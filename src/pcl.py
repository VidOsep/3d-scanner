import cv2
import numpy as np
from math import tan, radians
import os
from rotz import rotz

PATH = '/home/vid/3d-scanner-master/src/img/'


def GetLine(img, orig_img):
    """
    :param img: Thresholded line-image
    :param orig_img: Original image (no laser)
    :return:
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img[120:382,:]
    orig_img = orig_img[120:382,:]

    #for i in range(200):
    #    cv2.imwrite(os.path.join(PATH, 'cut_%04d.png' % int(slikaime[11:15])), img)

    ret, img = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)
    theta = 40.0
    rows, cols = img.shape
    points = np.empty(shape=(0,3))
    colors = np.empty(shape=(0,3))

    for i in range(rows):
        row = img[i,:]
        if row.argmax() != 0:
            peak = row.argmax()
        else:
            continue

        x = peak
        x = abs(cols/2-x)
        y = x/tan(radians(theta))
        point = np.array([x, y, rows-i])
        orig_row = orig_img[i,:]
        color = orig_row[peak]
        colors = np.vstack((colors,color[::-1]))
        points = np.vstack((points, point))
    return points, colors

def main():
    ANGLE_DIFF=360/200
    total_p = np.empty(shape=(0, 3))
    total_c = np.empty(shape=(0, 3))
    for k in range(200):
        pic_o = cv2.imread(PATH + 'image%04d.jpg'%(k))


        curr_angle = radians(k*ANGLE_DIFF)
        points,colors = GetLine(pic,pic_o,slikaime)

        R = rotz(curr_angle)
        points = points.dot(R)
        total_p = np.vstack((total_p, points))
        total_c = np.vstack((total_c, colors))
    return total_p,total_c

if __name__== '__main__':
    main()


