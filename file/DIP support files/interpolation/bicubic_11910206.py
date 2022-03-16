import cv2
import numpy as np
from scipy import interpolate


def bicubic_11910206(input_file, dim, raw=False):
    """
    Bicubic interpolation
    :param input_file: the file name that to be interpolated
    :param dim: a 1 x 2 vector('list' maybe used), specifying the row and column numbers of
    the interpolated image. The dimension of the interpolated image may be larger
     or smaller than that of the original image
    :param raw: used for direct test in .ipynb, if True, input_file is already a ndarray!
    This parameter default value is set as False
    :return: interpolated image array
    """
    assert input_file is not None  # error handling
    input_raw = input_file if raw else cv2.cvtColor(cv2.imread(input_file), cv2.COLOR_BGR2GRAY)
    resize_factor_h = input_raw.shape[0] / dim[0]
    resize_factor_w = input_raw.shape[1] / dim[1]
    return bicubic_scipy(input_raw, [resize_factor_h, resize_factor_w])


def bicubic_scipy(raw_gray_test, factor):  # TODO: test h and w sequence
    """
    Refer to: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp2d.html
    :return: interpolated image array
    """
    x = np.arange(raw_gray_test.shape[0])
    y = np.arange(raw_gray_test.shape[1])
    f = interpolate.interp2d(y, x, raw_gray_test, kind='cubic')
    xx = np.arange(0, raw_gray_test.shape[0], factor[0])
    yy = np.arange(0, raw_gray_test.shape[0], factor[1])
    interpolated = f(xx, yy)
    interpolated = interpolated.astype(int)
    return interpolated


test = np.uint8(np.random.randint(0, 255, size=(5, 7)))
resized = bicubic_11910206(test, (100, 100), raw=True)
