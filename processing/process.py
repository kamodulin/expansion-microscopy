import cv2
import numpy as np
import os
from skimage.morphology import remove_small_objects


def read_folder_volume(path):
    tiffs = [os.path.join(path, f) for f in os.listdir(path) if f[0] != '.']
    fnames = sorted(tiffs)
    
    vol = []

    for i, fname in enumerate(fnames):
        img = cv2.imread(fname, cv2.COLOR_BGR2GRAY)
        vol.append(img)

    vol = np.array(vol)

    return vol


def binarize(array, threshold_value):
    return (array > threshold_value)


def process_volume(path):
    vol = read_folder_volume(path)
    threshold = binarize(vol, 0.7)
    filtered = remove_small_objects(threshold, min_size=256, connectivity=3)

    return filtered