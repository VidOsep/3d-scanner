import os
import cv2
import numpy as np

# 3D scanned images folder:
im_dir = '/home/vid/3d-scanner-master/src/img/'

# Number of pictures taken for a single scan - increasing this also requires tuning on the raspberry pi's side
NUM_FRAMES = 200

def subtractAll(im_dir):
    """ Subtract whole set of images """
    # Undistort parameters
    mtx = np.array([[498.58640647, 0., 330.5688656],
                    [0., 501.24956248, 238.31721954],
                    [0., 0., 1.]])
    dst = np.array([[0.11690573, 0.48547085, 0.00312617, 0.0035685, -2.94301155]])

    # Perform subtraction on every single pair of images
    for frame in range(NUM_FRAMES):
        # Subtracts each individual image
        subtract(im_dir,frame)


def subtract(im_dir, index):
    # Subtract two images
    mtx = np.array([[498.58640647, 0., 330.5688656],
                    [0., 501.24956248, 238.31721954],
                    [0., 0., 1.]])
    dst = np.array([[0.11690573, 0.48547085, 0.00312617, 0.0035685, -2.94301155]])

    im_path_without = os.path.join(im_dir, 'subimage_%04d.jpg' % index)
    im_path_with = os.path.join(im_dir, 'image_%04d.jpg' % index)

    # Load images
    im_with = cv2.imread(im_path_with, cv2.IMREAD_COLOR)
    im_without = cv2.imread(im_path_without, cv2.IMREAD_COLOR)

    # subtract
    im_substr = cv2.subtract(im_without, im_with)
    im_substr = cv2.undistort(im_substr, mtx, dst, None)

    cv2.imwrite(os.path.join(im_dir, 'subtracted_%04d.png' % index), im_substr)

if __name__ == '__main__':
    subtractAll(im_dir)
