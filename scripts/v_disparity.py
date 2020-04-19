import disparity_utils as du
import cv2
import numpy as np

while True:
    
    image=du.create_test_disparity()
    v_disp=du.compute_v_disparity(image)
    u_disp=du.compute_u_disparity(image)
    
    image = cv2.applyColorMap(image, cv2.COLORMAP_JET)

    hough_v_disp= du.hough_lines(v_disp)
    hough_u_disp= du.hough_lines(u_disp)


    v_disp2 = np.hstack((hough_v_disp, v_disp))
    u_disp2 = np.vstack((hough_u_disp,u_disp))

    cv2.imshow('image', image)
    cv2.imshow('vhist_vis', v_disp2)
    cv2.imshow('uhist_vis', u_disp2)
    
    # cv2.imshow('hough_transform', hlines)

    # cv2.imwrite('disparity_image.png', image)
    # cv2.imwrite('v-disparity.png', vhist_vis)
    # cv2.imwrite('u-disparity.png', uhist_vis)


    if chr(cv2.waitKey(0)&255) == 'q':
        break