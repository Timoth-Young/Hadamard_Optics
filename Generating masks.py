import numpy as np
from matplotlib import pyplot
from PIL import Image


mask1 = np.zeros((1080,1920), np.uint8)

center = (960, 540)
radius = 336
Y, X, = np.ogrid[:1080, :1920]
dist_from_center = np.sqrt((X-center[0])**2+(Y-center[1])**2)
mask2 = dist_from_center <= radius

mask_Arr = np.ones((1080,1920), np.uint8)
mask_Arr[~mask2] = 0
mask_Arr = mask_Arr*255

pyplot.matshow(mask2)
pyplot.show()
pyplot.matshow(mask_Arr)
pyplot.show()