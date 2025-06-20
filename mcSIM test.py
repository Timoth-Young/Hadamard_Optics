# because I copied this over, IDK if all of these are necessary, but the code works and I don't want to find out
import datetime
import numpy as np
from pathlib import Path
import json
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from mcsim.expt_ctrl import dlp6500


# Connect to DMD
dmd = dlp6500.dlp6500win(debug=False)

# DMD Upoload Function
def Upload_Arr_to_DMD(mask,dmd):
    # the mask sent to the function needs to be an array with the dtype: uint8 N x Ny x Nx
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
                                                     bit_depth = 1, num_repeats = 0,
                                                     compression_mode = 'erle')
    dmd.set_pattern_sequence(img_inds, bit_inds, exposure_t, dark_t, triggered=False, clear_pattern_after_trigger= False, bit_depth=1, num_repeats=3, mode='on-the-fly')
    dmd.start_stop_sequence("start")


# Creating binary masks to build the pattern(s)
Y, X, = np.ogrid[:1080, :1920]
slant_vals = X + Y
print(slant_vals)
mask1 = slant_vals <= 1000
mask2 = abs(slant_vals-1500) <= 500
mask3 = slant_vals >= 2000

# Check masks to confirm shape
#matplotlib.pyplot.matshow(mask1)
#matplotlib.pyplot.show()

#matplotlib.pyplot.matshow(mask2)
#matplotlib.pyplot.show()

#matplotlib.pyplot.matshow(mask3)
#matplotlib.pyplot.show()

mask = np.array([mask1, mask2, mask3],np.uint8)

Upload_Arr_to_DMD(mask, dmd)
