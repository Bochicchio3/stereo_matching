
#%% 
import disparity_utils as du
import cv2
import numpy as np
from logging import FileHandler
from vlogging import VisualRecord
import logging

#%% 
image=cv2.imread('../images/carla_highres/disp_image_from_carla_simulator_high_res.png',0)

v_disp=du.compute_v_disparity(image)
u_disp=du.compute_u_disparity(image)

v_disp_mono=cv2.cvtColor(du.compute_v_disparity(image), cv2.COLOR_RGB2GRAY)
u_disp_mono=cv2.cvtColor(du.compute_u_disparity(image), cv2.COLOR_BGR2GRAY)

hough_v_disp, v_lines = du.hough_lines(v_disp_mono)
hough_u_disp, u_lines = du.hough_lines(u_disp_mono)


v_disp_with_hough = np.hstack((hough_v_disp, v_disp))
u_disp_with_hough = np.vstack((hough_u_disp,u_disp))

# %%

def treshold_u_disp(u_disparity, a, b, debug = False):
    
    for column_idx in range (0,u_disparity.shape[1]):
        tresh=int(a*abs(u_disparity.shape[1]/2-column_idx)/(u_disparity.shape[1]/2)+b) 
        for row_idx in range (tresh, u_disparity.shape[0]):
            u_disparity[row_idx,column_idx,:]=[255,255,0]
        # For debug purposes, you can visualize the treshold
        if debug:
            u_disparity[tresh, column_idx,:]=[0,0,0]
        
    return u_disparity


# %%
u_disp_tresholded=treshold_u_disp(u_disp, 65, 80, True)

# %%
image=cv2.imread('../images/carla_highres/disp_image_from_carla_simulator_high_res.png',0)

for i in range (0,image.shape[0]):
    for j in range (0,image.shape[1]):
        if image[i,j]< int(65*abs(image.shape[1]/2-j)/(image.shape[1]/2)+80):
            image[i,j]=0


# mask=image[i,j]<treshold
# image[mask]=0


# %%
v_disp=du.compute_v_disparity(image)
# v_disp_clean=cv2.cvtColor( v_disp, cv2.COLOR_BGR2GRAY)
v_disp_clean_hough, lines =du.hough_lines(v_disp)
# v_disp_clean_hough= cv2.cvtColor(v_disp_clean_hough , cv2.COLOR_BGR2GRAY)

# v_disp_clean_and_hough=np.hstack((v_disp_clean_hough, v_disp_clean))

#%%
# image = cv2.applyColorMap(image, cv2.COLORMAP_JET)

# image=np.hstack((v_disp2, image))
#%%
# image_rgb = cv2.applyColorMap(image, cv2.COLORMAP_JET)

while True:
    
    cv2.imshow('img', image)
    cv2.imshow('v_disp_cleaned', v_disp_clean_hough)
    cv2.imshow('u_disp', u_disp_tresholded)

    if chr(cv2.waitKey(0)&255) == 'q':
        break

cv2.destroyAllWindows()


# %%
