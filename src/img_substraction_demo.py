import os,sys
import cv2
import argparse

#im_dir = '/home/vid/Desktop/3dscanner/pictures'


parser = argparse.ArgumentParser()
parser.add_argument("im_dir", help='Dir with recored images', type=str)
args = parser.parse_args()

for frame in range(0, 274):
	# Set-up paths
	im_path_with = os.path.join(args.im_dir, 'without_laser_%04d.png'%frame)
	im_path_without = os.path.join(args.im_dir, 'with_laser_%04d.png'%frame)

	# Load images
	im_with = cv2.imread(im_path_with,cv2.IMREAD_COLOR)
	im_without = cv2.imread(im_path_without,cv2.IMREAD_COLOR)

	# Display images
	#cv2.imshow('with',im_with)
	#cv2.imshow('without',im_without)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

	# subtract
	im_substr = cv2.subtract(im_without, im_with)
	cv2.imwrite(os.path.join(args.im_dir,'subtracted_%04d.png'%frame), im_substr)
        #cv2.imshow('subtracted', im_substr)
        #cv2.waitKey(0)
	#cv2.destroyAllWindows()
