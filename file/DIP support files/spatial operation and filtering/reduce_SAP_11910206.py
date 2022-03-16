import numpy as np
import cv2


def order_filter(arr, n_size, pad_mode='constant'):
    """
    Implement order statistic filter (median-value filter)

    :param arr: the input image or array
    :param n_size: is the scale of the filter size
    :param pad_mode: refer to `np.pad`
    :return: result of order filtering
    """
    assert n_size % 2 == 1  # only handel odd kernel
    _H = arr.shape[0]
    _W = arr.shape[1]
    _half = n_size // 2
    _l_half = _half + 1
    padded = np.pad(arr, (_half, _half), mode=pad_mode)
    order_filtered = np.zeros_like(arr)
    for i in range(_half, _H):
        for j in range(_half, _W):
            order_filtered[i - 1, j - 1] = np.median(padded[i - _half:i + _l_half, j - _half:j + _l_half])
    return order_filtered


def reduce_SAP_11910206(input_image, n_size):
    img_arr = cv2.cvtColor(cv2.imread(input_image), cv2.COLOR_RGB2GRAY)
    return order_filter(img_arr, n_size)
