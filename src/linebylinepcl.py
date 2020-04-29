from pcl import GetLine
from export_ply import write_ply
from rotz import rotz
from numpy import np
import cv2
from math import radians
import os.path
import time
from img_substraction_demo import subtract

PATH = '/home/vid/3d-scanner-master/src/img/'

NUM_FRAMES = 200

def main():
    ANGLE_DIFF=360/NUM_FRAMES  # Degrees on a single turn
    total_p = np.empty(shape=(0, 3))  # X Y Z pos of point in point-cloud
    total_c = np.empty(shape=(0, 3))  # R G B val of point in point-cloud

    # Export mesh line by line
    for k in range(NUM_FRAMES):
        # The program waits until the images are taken
        while not os.path.isfile(PATH + 'image%04d.jpg'%k) and os.path.isfile(PATH + "subimage%04d.jpg"%k):
            time.sleep(0.1)
        subtract(PATH, k)
        pic = cv2.imread(PATH + 'image%04d.jpg'%k)
        pic_o = cv2.imread(PATH + 'subtracted_%04d.jpg'%k)

        curr_angle = radians(k*ANGLE_DIFF) # Current angle in radians
        points,colors = GetLine(pic,pic_o) # Get the point-cloud at this point

        R = rotz(curr_angle)
        points = points.dot(R)

        total_p = np.vstack((total_p, points))
        total_c = np.vstack((total_c, colors))

        write_ply(total_p,total_c,'subtracted_%04d.ply'%k)