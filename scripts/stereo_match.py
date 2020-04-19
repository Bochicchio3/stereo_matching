#!/usr/bin/env python

'''
Simple example of stereo image matching.
'''


import numpy as np
import cv2 as cv

def main():
    print('loading images...')
    
    imgL = cv.pyrDown(cv.imread('./images/cones/im2.png')) # downscale images for faster processing
    imgR = cv.pyrDown(cv.imread('./images/cones/im6.png'))

    # disparity range is tuned for 'aloe' image pair
    window_size = 3
    min_disp = 8
    num_disp = 16-min_disp
    stereo = cv.StereoSGBM_create(minDisparity = min_disp,
        numDisparities = num_disp,
        blockSize = 4,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2,
        disp12MaxDiff = 1,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange = 32
    )

    print('computing disparity...')
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0
    # disp=cv.convertScaleAbs(disp, alpha=255)
    # print (disp)
    cv.imshow('left', imgL)
    cv.imshow('disparity', (disp-min_disp)/num_disp)
    cv.waitKey()

    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()
