import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import tan, radians
import struct

PATH = '/home/vid/projekti/3dsc/pics/'

def make_axis_rotation_matrix(direction, angle):
    """
    Create a rotation matrix corresponding to the rotation around a general
    axis by a specified angle.

    R = dd^T + cos(a) (I - dd^T) + sin(a) skew(d)

    Parameters:

        angle : float a
        direction : array d
    """
    d = np.array(direction, dtype=np.float64)
    d /= np.linalg.norm(d)

    eye = np.eye(3, dtype=np.float64)
    ddt = np.outer(d, d)
    skew = np.array([[0, d[2], -d[1]],
                     [-d[2], 0, d[0]],
                     [d[1], -d[0], 0]], dtype=np.float64)

    mtx = ddt + np.cos(angle) * (eye - ddt) + np.sin(angle) * skew
    return mtx

def GetLine(img,orig_img, curr_angle):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, img = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)
    theta = 32
    w,h = img.shape
    points = np.empty(shape=(0,3))
    #colors = np.empty(shape=(0,3))

    for i in range(w):
        row = img[i,:]
        if row.argmax() != 0:
            peak = row.argmax()
        else:
            peak = 0
            color = 0
            pass

        M = make_axis_rotation_matrix([0,0,1], curr_angle)

        x = peak
        y = x/tan(radians(theta))
        point = np.array([x,y,h-i])
        #color = np.array([orig_img[i,x]])
        points = np.vstack((points,M.dot(point)))
        #colors = np.vstack((colors,color))

        #points = M.dot(points) # np.transpose(points)
    return points,None




def main():

    ANGLE_DIFF=3.6
    '''
    def visualize_pcl(points, colors):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.axis('equal')
        points = np.array(points)


        ax.scatter(points[:,0], points[:,1], points[:,2],)
        plt.show()
    '''
    total_p = np.empty(shape=(0,3))
    total_c = np.empty(shape=(0,3))
    for k in range(100):
        if k < 10:
            pic = cv2.imread(PATH + 'subtracted_000' + str(k) + '.png')
        else:
            pic = cv2.imread(PATH + 'subtracted_00' + str(k) + '.png')
        pic_o = cv2.imread(PATH + 'image' + str(k) + '.jpg')
        points,colors = GetLine(pic,pic_o, radians(k*ANGLE_DIFF))
        total_p = np.vstack((total_p,points))
        #total_c = np.vstack((total_c, colors))
    return total_p

main()


