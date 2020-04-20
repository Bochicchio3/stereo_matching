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
    
image=cv2.imread('../images/carla_highres/disp_image_from_carla_simulator_high_res.png',0)

v_disp=cv2.Canny(du.compute_v_disparity(image),50,200)
u_disp=cv2.Canny(du.compute_u_disparity(image),50,200)

image = cv2.applyColorMap(image, cv2.COLORMAP_JET)

hough_v_disp= du.hough_lines(v_disp)
hough_u_disp= du.hough_lines(u_disp)

#Binarization:


#Projection and classification in the image space


# v_disp2 = np.hstack((hough_v_disp, v_disp))
# u_disp2 = np.vstack((hough_u_disp,u_disp))

#%% 

filler=np.zeros((u_disp2.shape[0], v_disp2.shape[1]), dtype=np.uint8)

logger.debug(VisualRecord(
    "U_disparity", [filler,  u_disp2 , v_disp2, image], fmt="png"))
# logger.debug(VisualRecord(
#     "V_disparity and Image depth map", [v_disp2, image],  fmt="png"))
#%% 

    
drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv2.rectangle(v_disp,(ix,iy),(x,y),(0,255,0),-1)
            else:
                cv2.circle(v_disp,(x,y),5,(0,0,255),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(v_disp,(ix,iy),(x,y),(0,255,0),-1)
        else:
            cv2.circle(v_disp,(x,y),5,(0,0,255),-1)  
    # cv2.imshow('vhist_vis', v_disp2)
    # cv2.imshow('uhist_vis', u_disp2)

    # cv2.imshow('hough_transform', hlines)

    # cv2.imwrite('disparity_image.png', image)
    # cv2.imwrite('v-disparity.png', vhist_vis)
    # cv2.imwrite('u-disparity.png', uhist_vis)

cv2.namedWindow('v_disp')
cv2.setMouseCallback('v_disp',draw_circle)

#%%

while True:

    cv2.imshow('v_disp', v_disp)
    # cv2.imshow('u_disp', u_disp)

    if chr(cv2.waitKey(0)&255) == 'q':
        break

cv2.destroyAllWindows()


# %%
