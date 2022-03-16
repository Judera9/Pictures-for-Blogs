import numpy as np
import cv2


def hist(arr, _min=0, _max=255, parallel=1):
    """
    Use a tricky method with the efficient numpy. Avoid using for loop twice to iterate the image, because it is slow!

    :param parallel: 0 means that arr is single image or array, otherwise it is an array of multiple images or arrays
    :param arr: the input image or array
    :param _min: minimum value of arr
    :param _max: maximum value of arr
    :return: histogram bins with size of (parallel x _max - _min + 1)
    """
    _hist = None
    if parallel == 1:
        _hist = np.zeros(_max - _min + 1)
        for v in range(_min, _max + 1):
            _hist[v] = np.sum(arr == v)
    else:
        _hist = np.zeros((parallel, _max - _min + 1))
        for v in range(_min, _max + 1):
            _hist[:, v] = np.sum(arr == v, axis=1)
    return _hist


# Q3_2.tif

def hist_match(arr, spec_hist):
    """
    Implementation of histogram match (regulation)

    :param arr: the input image or array
    :param spec_hist: is a list containing a specified histogram of the input image (the designed z_q PDF)
    :return: matched array or image
    """
    input_hist = hist(arr.ravel())
    s_k = np.round(255 / np.sum(input_hist) * np.cumsum(input_hist))
    z_q2s_k = np.round(255 * np.cumsum(spec_hist))
    output_image = np.zeros_like(arr)
    for i in range(256):  # r -> s
        idx = np.where(s_k[i] <= z_q2s_k)[0][0]  # s -> z
        output_image[arr == i] = idx
    output_hist = hist(output_image.ravel())
    return output_image, output_hist, input_hist


def hist_match_11910206(input_image, spec_hist):
    img_arr = cv2.cvtColor(cv2.imread(input_image), cv2.COLOR_RGB2GRAY)
    return hist_match(img_arr, spec_hist)
