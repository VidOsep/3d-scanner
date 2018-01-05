import numpy as np
import cv2
import glob
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("im_dir", help='Dir with calib. images', type=str)
args = parser.parse_args()

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob(os.path.join(args.im_dir,'checkerboard*.png'))

if len(images) <= 0:
    raise Exception('No pattern images found!')

for fname in images:
	print ('Loading %s ...'%fname)
	im_path = os.path.join(args.im_dir, fname)
	img = cv2.imread(im_path)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	#cv2.imshow('img_orig',gray)
	#cv2.waitKey(500)

	# Find the chess board corners
	ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

	# print (corners)
	# print (ret)

	# If found, add object points, image points (after refining them)
	if not ret:
		print ('Error, corners not found ...')
	else:
		print ('Corners found!')
		objpoints.append(objp)

		corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		imgpoints.append(corners2)

		# Draw and display the corners
		img = cv2.drawChessboardCorners(img, (9,6), corners2,ret)
		cv2.imshow('img',img)
		cv2.waitKey(500)

		#ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objp, corners2, gray.shape[::-1],None,None)


cv2.destroyAllWindows()
