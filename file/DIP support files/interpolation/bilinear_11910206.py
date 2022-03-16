import cv2
import numpy as np


def bilinear_11910206(input_file, dim, raw=False, method='default'):
    """
    Bilinear interpolation
    :param input_file: the file name that to be interpolated
    :param dim: a 1 x 2 vector('list' maybe used), specifying the row and column numbers of
    the interpolated image. The dimension of the interpolated image may be larger or
    smaller than that of the original image
    :param raw: used for direct test in .ipynb, if True, input_file is already a ndarray!
    This parameter default value is set as False
    :param method: choice are default (linear2), polyfit, only supported for gray
    :return: interpolated image array
    """

    assert input_file is not None  # error handling
    input_raw = input_file if raw else cv2.cvtColor(cv2.imread(input_file), cv2.COLOR_BGR2GRAY)
    assert input_raw.ndim == 2 or input_raw.ndim == 3

    raw_h = input_raw.shape[0]
    raw_w = input_raw.shape[1]
    resize_factor_h = raw_h / dim[0]
    resize_factor_w = raw_w / dim[1]
    init_h = 0.5 * resize_factor_h - 0.5
    init_w = 0.5 * resize_factor_w - 0.5
    max_limit_h = raw_h - 1
    max_limit_w = raw_w - 1
    margin_limit_h = np.floor(0.5 / resize_factor_h + 0.5).astype(int)
    margin_limit_w = np.floor(0.5 / resize_factor_w + 0.5).astype(int)

    if input_raw.ndim == 2:
        interpolated = np.zeros((dim[0], dim[1]), dtype=int)

        interpolated[:margin_limit_h, :margin_limit_w] = input_raw[0, 0]
        interpolated[:margin_limit_h, -1:-margin_limit_w - 1:-1] = input_raw[0, max_limit_w]
        interpolated[-1:-margin_limit_h - 1:-1, :margin_limit_w] = input_raw[max_limit_h, 0]
        interpolated[-1:-margin_limit_h - 1:-1, -1:-margin_limit_w - 1:-1] = input_raw[max_limit_h, max_limit_w]

        for j in range(margin_limit_w, dim[1] - margin_limit_w):
            y = init_w + resize_factor_w * j
            y1 = np.floor(y).astype(int)
            y2 = np.ceil(y).astype(int)
            interpolated[:margin_limit_h, j] = (y2 - y) * input_raw[0, y1] + (y - y1) * input_raw[0, y2]
            interpolated[-1:-margin_limit_h - 1:-1, j] = (y2 - y) * input_raw[max_limit_h, y1] + (
                    y - y1) * input_raw[max_limit_h, y2]

        for i in range(margin_limit_h, dim[0] - margin_limit_h):
            x = init_h + resize_factor_h * i
            x1 = np.floor(x).astype(int)
            x2 = np.ceil(x).astype(int)
            interpolated[i, :margin_limit_w] = (x2 - x) * input_raw[x1, 0] + (x - x1) * input_raw[x2, 0]
            interpolated[i, -1:-margin_limit_w - 1:-1] = (x2 - x) * input_raw[x1, max_limit_w] + (
                    x - x1) * input_raw[x2, max_limit_w]

        for i in range(margin_limit_h, dim[0] - margin_limit_h):
            for j in range(margin_limit_w, dim[1] - margin_limit_w):
                x = init_h + resize_factor_h * i
                y = init_w + resize_factor_w * j
                x1 = np.floor(x).astype(int)
                y1 = np.floor(y).astype(int)
                x2 = np.ceil(x).astype(int)
                y2 = np.ceil(y).astype(int)

                if method is 'polyfit':
                    interpolated[i, j] = (np.array([[x2 * y2, -x2 * y1, -x1 * y2, x1 * y1],
                                                   [-y2, y1, y2, -y1],
                                                   [-x2, x2, x1, -x1],
                                                   [1, -1, -1, 1]]) @ np.array(
                        [[input_raw[x1, y1]],
                         [input_raw[x1, y2]],
                         [input_raw[x2, y1]],
                         [input_raw[x2, y2]]])).reshape(1, 4) @ np.array([[1], [x], [y], [x * y]])
                else:
                    interpolated[i, j] = (np.array([[x2 - x, x - x1]]) @ np.array(
                        [[input_raw[x1, y1], input_raw[x1, y2]],
                         [input_raw[x2, y1], input_raw[x2, y2]]]) @ np.array([[y2 - y], [y - y1]])).astype(int)
    else:
        interpolated = np.zeros((dim[0], dim[1], 3), dtype=int)

        interpolated[:margin_limit_h, :margin_limit_w, :] = input_raw[0, 0, :]
        interpolated[:margin_limit_h, -1:-margin_limit_w - 1:-1, :] = input_raw[0, max_limit_w, :]
        interpolated[-1:-margin_limit_h - 1:-1, :margin_limit_w, :] = input_raw[max_limit_h, 0, :]
        interpolated[-1:-margin_limit_h - 1:-1, -1:-margin_limit_w - 1:-1, :] = input_raw[max_limit_h, max_limit_w, :]

        for j in range(margin_limit_w, dim[1] - margin_limit_w):
            y = init_w + resize_factor_w * j
            y1 = np.floor(y).astype(int)
            y2 = np.ceil(y).astype(int)
            interpolated[:margin_limit_h, j, :] = (y2 - y) * input_raw[0, y1, :] + (y - y1) * input_raw[0, y2, :]
            interpolated[-1:-margin_limit_h - 1:-1, j, :] = (y2 - y) * input_raw[max_limit_h, y1, :] + (
                    y - y1) * input_raw[max_limit_h, y2, :]

        for i in range(margin_limit_h, dim[0] - margin_limit_h):
            x = init_h + resize_factor_h * i
            x1 = np.floor(x).astype(int)
            x2 = np.ceil(x).astype(int)
            interpolated[i, :margin_limit_w, :] = (x2 - x) * input_raw[x1, 0, :] + (x - x1) * input_raw[x2, 0, :]
            interpolated[i, -1:-margin_limit_w - 1:-1, :] = (x2 - x) * input_raw[x1, max_limit_w, :] + (
                    x - x1) * input_raw[x2, max_limit_w, :]

        for i in range(margin_limit_h, dim[0] - margin_limit_h):
            for j in range(margin_limit_w, dim[1] - margin_limit_w):
                x = init_h + resize_factor_h * i
                y = init_w + resize_factor_w * j
                x1 = np.floor(x).astype(int)
                y1 = np.floor(y).astype(int)
                x2 = np.ceil(x).astype(int)
                y2 = np.ceil(y).astype(int)

                for c in range(3):
                    interpolated[i, j, c] = (np.array([[x2 - x, x - x1]]) @ np.array(
                        [[input_raw[x1, y1, c], input_raw[x1, y2, c]],
                         [input_raw[x2, y1, c], input_raw[x2, y2, c]]]) @ np.array([[y2 - y], [y - y1]])).astype(int)

    return interpolated
