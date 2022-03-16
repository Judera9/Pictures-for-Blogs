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


def hist_equ(arr, local=False):
    """
    Implement histogram equalization

    :param local: means whether calculate in parallel style
    :param arr: the input image or array
    :return: output image, output histogram bins, input histogram bins
    """
    if not local:
        input_hist = hist(arr.ravel())
        r_pdf = np.array(input_hist) / np.sum(input_hist)
        r_cdf = np.round(255 * np.cumsum(r_pdf))
        output_image = np.zeros_like(arr)
        for idx in range(256):
            output_image[arr == idx] = r_cdf[idx]
        output_hist = hist(output_image.ravel())
        return output_image, output_hist, input_hist
    else:
        _parallel = arr.shape[0]  # number of neighbors
        _m2 = arr.shape[1]  # size of neighbors, m^2
        _half = _m2 // 2
        input_hist = hist(arr, parallel=_parallel)
        r_pdf = input_hist / _m2
        r_cdf = np.round(255 * np.cumsum(r_pdf, axis=1))
        output_image = np.zeros(_parallel)
        center_pixel = arr[:, _m2 // 2].astype(int)
        for i in range(_parallel):
            output_image[i] = r_cdf[i, center_pixel[i]]
        return output_image


def img2big_mat(arr, m_size, pad_mode='constant'):
    """
    calculate all the neighbors by iterating the array

    :param pad_mode: refer to definition of `np.pad`, 'edge', 'reflect', 'symmetric' are commonly used pad methods
    :param pad: whether pad the arr after m_size, default is yes
    :param arr: the input image or array
    :param m_size: is the scale of the neighborhood size
    :return: the padded arr, and a (pixel_cnt x m_size**2) size array contains all neighbors
    """

    _H = arr.shape[0]
    _W = arr.shape[1]
    assert _H >= m_size and _W >= m_size
    _half = m_size // 2
    _l_half = _half + 1
    _padded = np.pad(arr, (_half, _half), mode=pad_mode)
    big_mat = np.zeros((_H * _W, m_size * m_size))
    cnt = 0
    for i in range(_half, _H + _half):
        for j in range(_half, _W + _half):
            big_mat[cnt] = _padded[i - _half:i + _l_half, j - _half:j + _l_half].ravel()
            cnt += 1
    return _padded, big_mat


def local_hist_equ(arr, m_size):
    """
    Implementation of local histogram equalization

    :param arr: the input image or array
    :param m_size: is the scale of the neighborhood size
    :return: output_image, output_hist, input_hist
    """
    input_hist = hist(arr)
    _, _big_mat = img2big_mat(arr, m_size)
    output_image = hist_equ(_big_mat, local=True).reshape(arr.shape[0], arr.shape[1])
    output_hist = hist(output_image)
    return output_image, output_hist, input_hist


def local_hist_equ_11910206(input_image, m_size):
    img_arr = cv2.cvtColor(cv2.imread(input_image), cv2.COLOR_RGB2GRAY)
    return local_hist_equ(img_arr, m_size)
