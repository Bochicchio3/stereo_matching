
#%% 

import disparity_utils as du
import cv2
import numpy as np
from logging import FileHandler
from vlogging import VisualRecord
import logging

logger = logging.getLogger("demo")
fh = FileHandler('test.html', mode="w")
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

# while True:

    # image=du.create_test_disparity()
#%% 
image=cv2.imread('../images/carla_highres/disp_image_from_carla_simulator_high_res.png',0)
#%% 
v_disp=du.compute_v_disparity(image)
u_disp=du.compute_u_disparity(image)

# v_disp=cv2.Canny(du.compute_v_disparity(image),50,200)
# u_disp=cv2.Canny(du.compute_u_disparity(image),50,200)


image = cv2.applyColorMap(image, cv2.COLORMAP_JET)

hough_v_disp= du.hough_lines(v_disp)
hough_u_disp= du.hough_lines(u_disp)


# v_disp2 = np.hstack((hough_v_disp, v_disp))
# u_disp2 = np.vstack((hough_u_disp,u_disp))

#%%

while True:
    
    cv2.imshow('img', image)

    # cv2.imshow('v_disp', v_disp)
    cv2.imshow('u_disp', u_disp)

    if chr(cv2.waitKey(0)&255) == 'q':
        break

cv2.destroyAllWindows()


# %%

def treshold(column, idx, a=10, b=5):
    return int(a*abs(column/2-idx)/(column/2)+b)

def treshold_u_disp(u_disparity, a, b):
    # binarized = np.zeros(u_disparity.shape)
    for column_idx in range (0,u_disparity.shape[1]):
        tresh=treshold(u_disparity.shape[1], column_idx, a = 35, b = 30) 
        for row_idx in range (tresh, u_disparity.shape[0]):
            u_disparity[row_idx,column_idx,:]=[0,0,0]
        u_disparity[tresh, column_idx,:]=[255,255,0]
        
    return u_disparity

# %%
u_disp=treshold_u_disp(u_disp, 65, 50)

# %%
# Backprojection

image=cv2.imread('../images/carla_highres/disp_image_from_carla_simulator_high_res.png',0)

for i in range (0,image.shape[0]):
    for j in range (0,image.shape[1]):
        if image[i,j]< treshold(image.shape[1],j, 65,80):
            image[i,j]=0
        # else:
        #     image[i,j]=0

v_disp=du.compute_v_disparity(image)
hough_v_disp= du.hough_lines(v_disp)
v_disp2 = np.hstack((hough_v_disp, v_disp))


#%%
image = cv2.applyColorMap(image, cv2.COLORMAP_JET)

image=np.hstack((v_disp2, image))
#%%

while True:
    
    cv2.imshow('img', image)

    # cv2.imshow('v_disp', v_disp)
    # cv2.imshow('u_disp', u_disp)

    if chr(cv2.waitKey(0)&255) == 'q':
        break

cv2.destroyAllWindows()


# %%
