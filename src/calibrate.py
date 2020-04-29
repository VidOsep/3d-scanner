import cv2
import os
import numpy as np

PATH = '/home/vid/3d-scanner-master/src/bimg/'
files = os.listdir(PATH)
pattern_size = (9, 6)
pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
debug_dir = '/home/vid/3d-scanner-master/src/bimg/debugdir/'

del files[-1]
print(files)

for fn in files:
    obj_points = []
    img_points = []
    h, w = cv2.imread(os.path.join(PATH,fn), cv2.IMREAD_GRAYSCALE).shape[:2]
    print 'processing %s...' % fn,
    img = cv2.imread(fn, 0)
    if img is None:
        print("Failed to load\n")
    path, fn = os.path.split(fn)
    name, ext = os.path.splitext(fn)
    found, corners = cv2.findChessboardCorners(img, pattern_size)
    if found:
        term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
        cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)
    if debug_dir:
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.drawChessboardCorners(vis, pattern_size, corners, found)
        cv2.imwrite('%s/%s_chess.bmp' % (debug_dir, name), vis)
    if not found:
        print 'chessboard not found'
        continue
    img_points.append(corners.reshape(-1, 2))
    obj_points.append(pattern_points)

    print 'ok'