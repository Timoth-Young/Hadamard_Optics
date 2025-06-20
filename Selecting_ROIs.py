# trying to select ROIS with some mouse events, and then load them onto the DMD

import cv2
import numpy as np
import json
import matplotlib
matplotlib.use('TKAGG')
from matplotlib import pyplot as plt
from scipy.linalg import hankel
from mcsim.expt_ctrl import dlp6500

#connect to DMD
dmd = dlp6500.dlp6500win(debug=False)

# DMD Upoload Function
def Upload_Arr_to_DMD(mask,dmd):
    # the mask sent to the function needs to be an array with the dtype: uint8 and dimensions:N x Ny x Nx
    pat = mask
    # Exposure time in microseconds
    exposure_t = 250000
    # Dark time in microseconds
    dark_t = 0
    # Should the DMD wait to recieve a "trigger" signal? Y/N
    triggered = False
    img_inds, bit_inds = dmd.upload_pattern_sequence(pat,
                                                     exposure_t,
                                                     dark_t,
                                                     triggered,
                                                     clear_pattern_after_trigger = False,
                                                     bit_depth = 1,
                                                     num_repeats = 0)
    dmd.set_pattern_sequence(img_inds, bit_inds, exposure_t, dark_t, triggered=False, clear_pattern_after_trigger= False, bit_depth=1, num_repeats=0, mode='on-the-fly')
    dmd.start_stop_sequence("start")

Size = (1080, 1920)
# DMD size in pixels, needs to be 1080X1920 or the DMD glitches out

# placeholder for an initial frame, once the camera is set up, load the frame
# depending on camera resolution there might have to be a size conversion, figure that out later
blank = np.zeros(Size, np.uint8)
S = cv2.selectROIs('select ROIS', blank)

# I feel like I'm going crazy, so check how ROIs are stored in S
#print(S)
#print(len(S))
#print(S[0])
#print(S[1])

# I want to make a mask with the coordinates in S[0]
#mask1 = np.zeros(Size, np.uint8)
#mask1 = cv2.rectangle(mask1, (ROI1[0],ROI1[1]), (ROI1[0]+ROI1[2], ROI1[1]+ROI1[3]) , (255, 255, 255), -1)
#mask2 = np.zeros(Size, np.uint8)
#mask2 = cv2.rectangle(mask2, (ROI2[0],ROI2[1]), (ROI2[0]+ROI2[2], ROI2[1]+ROI2[3]) , (255, 255, 255), -1)
#mask3 = np.zeros(Size, np.uint8)
#mask3 = cv2.rectangle(mask3, (ROI3[0],ROI3[1]), (ROI3[0]+ROI3[2], ROI3[1]+ROI3[3]) , (255, 255, 255), -1)

# Moving mask building to a for loop so that the number of ROIs is arbitrary
# for i from 0 to len[S]
# mask_blank = np.zeros(Size, np.uint8)
# mask_roi = cv2.rectangle(mask_blank, (x,y), (x+width, y+height) , (255, 255, 255), -1)

masks = np.zeros((len(S), 1080, 1920), np.uint8)

for i in range(len(S)):
    mask = np.zeros(Size, np.uint8)
    ROI = S[i]
    # ROI[0] = x
    # ROI[1] = y
    # ROI[2] = width
    # ROI[3] = height
    masks[i] = cv2.rectangle(mask, (ROI[0],ROI[1]), (ROI[0]+ROI[2], ROI[1]+ROI[3]) , (255, 255, 255), -1)
    plt.matshow(masks[i])
    plt.show()

All_masks = np.sum(masks, 0)
plt.matshow(All_masks)
plt.show()

if len(S) == 3:
    # Encode matrix, technically there also needs to be an "off" frame in the encode, but I can't see that rn
    E = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 0]], np.uint8)
    seq = np.zeros([4, 1080, 1920], np.uint8)
    for j in range(3):
        seq[j+1] = E[j,0]*masks[0] | E[j,1]*masks[1] | E[j,2]*masks[2]
    fig1 = plt.matshow(seq[0])
    fig2 = plt.matshow(seq[1])
    fig3 = plt.matshow(seq[2])
    fig4 = plt.matshow(seq[3])
    plt.show()

elif len(S) <= 7:
    # Encode matrix, technically there also needs to be an "off" frame in the encode, but I can't see that rn
    E = hankel([1,1,1,0,1,0,0],[0,1,1,1,0,1,0])
    seq =  np.zeros([8, 1080, 1920], np.uint8)
    if len(S) < 7:
        for k in range(len(S), 7):
            masks = np.append(masks, np.zeros([1,1080,1920], np.uint8),0)
    for j in range(7):
        seq[j+1] = E[j,0]*masks[0]|E[j,1]*masks[1]|E[j,2]*masks[2]|E[j,3]*masks[3]|E[j,4]*masks[4]|E[j,5]*masks[5]|E[j,6]*masks[6]

seq = seq/255
seq = seq.astype(np.uint8)
print(str(seq.dtype))
Upload_Arr_to_DMD(seq, dmd)
