"""
V_disparity
=====
Disparity Utils functions

Provides
  1. Compute V_disparity
  2. Compute U_disparity
  3. Draw objects
  4. Create test Disparity

Implementation
----------------------------
The implementation is simply the histogram of each raw in the disparity map
Example code:

  >>> v_disp= compute_v_disparity(img, max_disp)

"""

import cv2
import numpy as np
import time
import sys
import math

def compute_v_disparity(img, max_disp=255):
    
    """
    V_disparity
    ----
    It outputs the v_disparity of the input image.
    The algorithm calculates the histogram of each line

    Parameters
    ----------
    img:  input image

    Returns
    -------
    v_disparity
    """

    
    v_disp = np.zeros((img.shape[0], max_disp), np.float)
    for i in range(img.shape[0]):
        v_disp[i, ...] = cv2.calcHist(images=[img[i, ...]], channels=[0], mask=None, histSize=[max_disp],
                                        ranges=[0, max_disp]).flatten() / float(img.shape[0])
        
    # v_disp = cv2.convertScaleAbs(v_disp,alpha=255)
    v_disp = np.array(v_disp * 255, np.uint8)
    v_disp = cv2.applyColorMap(v_disp, cv2.COLORMAP_JET)
    v_disp[v_disp < 5] = 0
    
    return v_disp


def compute_u_disparity(img, max_disp=255):
    """
    Compute U disparity
    --

    Parameters
    ----------
    img: input image
    
    max_disp: 

    Returns
    -------
    u_disp: 
    """
    u_disp = np.zeros((max_disp, img.shape[1] ), np.float)
    for i in range(img.shape[1]):
        u_disp[..., i] = cv2.calcHist(images=[img[..., i]], channels=[0], mask=None, histSize=[max_disp],
                                            ranges=[0, max_disp]).flatten() / float(img.shape[1])

    u_disp = cv2.convertScaleAbs(u_disp, alpha = 255)
    # u_disp = np.array(u_disp * 255, np.uint8)
    u_disp = cv2.applyColorMap(u_disp, cv2.COLORMAP_JET)
    u_disp[ u_disp < 5] = 0
    
    return u_disp


def draw_object(image, x, y, width=50, height=100):
    """
    Utility function to draw (width x height pixel blocks on a image).

    Parameters
    ----------
    image: input image
    x: x position
    y: y position
    width=50: default width of block
    height=100: default heigth of block

    Returns
    -------
    image with blocks

    """
    color = image[y, x]
    image[y-height:y, x-width//2:x+width//2] = color
    
    
def create_test_disparity(IMAGE_HEIGHT = 600, IMAGE_WIDTH = 800, max_disp=200):
    """
    Create a Test disparity with a gradient and some colored blocks

    Parameters
    ----------
    IMAGE_HEIGHT=600: 
    IMAGE_WIDTH=800: 

    Returns
    -------
    Test disparity image
    
    """

    image = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH), np.uint8)

    for c in range(IMAGE_HEIGHT)[::-1]:
        image[c, ...] = int(float(c) / IMAGE_HEIGHT * max_disp)

        draw_object(image, 275, 175)
        draw_object(image, 300, 200)
        draw_object(image, 100, 350)


    return image


'''
This example illustrates how to use Hough Transform to find lines

Usage:
    houghlines.py [<image_name>]
    image argument defaults to pic1.png
'''



def hough_lines(img, probabilistic=True):
    """
    Find hough lines in the image. 

    Parameters
    ----------
    img: input image
    probabilistic=True: if True, use the Probabilistic method. Use the standard method otherwise

    Returns
    -------
    cdst: output an images with the lines.

    """
    dst = cv2.Canny(img, 50, 200)
    
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    if probabilistic: # HoughLinesP
        lines = cv2.HoughLinesP(dst, 1, math.pi/180.0, 40, np.array([]), 50, 10)
        a, b, _c = lines.shape
        for i in range(a):
            cv2.line(cdst, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)

    else:    # HoughLines
        lines = cv2.HoughLines(dst, 1, math.pi/180.0, 50, np.array([]), 0, 0)
        if lines is not None:
            a, b, _c = lines.shape
            for i in range(a):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0, y0 = a*rho, b*rho
                pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
                pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
                cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
    return cdst


