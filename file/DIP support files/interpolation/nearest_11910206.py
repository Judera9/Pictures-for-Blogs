import cv2
import numpy as np
from matplotlib import pyplot as plt


def nearest_11910206(input_file, dim, raw=False):
    """
    Nearest neighbor interpolation
    :param input_file: the file name that to be interpolated
    :param dim: a 1 x 2 vector('list' maybe used), specifying the row and column numbers
    of the interpolated image. The dimension of the interpolated image may be larger or
    smaller than that of the original image
    :param raw: used for direct test in .ipynb, if True, input_file is already a ndarray!
    This parameter default value is set as False
    :return: interpolated image array
    """

    assert input_file is not None  # error handling
    input_raw = input_file if raw else cv2.cvtColor(cv2.imread(input_file), cv2.COLOR_BGR2GRAY)
    assert input_raw.ndim == 2 or input_raw.ndim == 3
    resize_factor_h = input_raw.shape[0] / dim[0]
    resize_factor_w = input_raw.shape[1] / dim[1]
    interpolated = np.zeros(dim, dtype=int) if input_raw.ndim == 2 else np.zeros((dim[0], dim[1], 3), dtype=int)
    init_h = 0.5 * resize_factor_h - 0.5
    init_w = 0.5 * resize_factor_w - 0.5
    for i in range(dim[0]):
        for j in range(dim[1]):
            r_idx = np.round(init_h + resize_factor_h * i).astype(int)
            c_idx = np.round(init_w + resize_factor_w * j).astype(int)
            if input_raw.ndim == 2:
                interpolated[i, j] = input_raw[r_idx, c_idx]
            else:
                interpolated[i, j, :] = input_raw[r_idx, c_idx, :]

    return interpolated
