---
title: Image Interpolation
date: 2022-03-04 19:51:57
math: true
categories:
- [课程相关, DIP]
tags:
- 图像插值
- DIP
- NumPy
index_img: https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_11910206_14_0.png
banner_img: /img/default3.png
comment: 'valine'
---

# Image Interpolation

- [Image Interpolation](#image-interpolation)
  - [Objectives](#objectives)
  - [Principle](#principle)
    - [Geometric Center Alignment](#geometric-center-alignment)
    - [Nearest Neighbor Interpolation](#nearest-neighbor-interpolation)
      - [Derivation](#derivation)
      - [Pseudo Code](#pseudo-code)
    - [Bilinear Interpolation](#bilinear-interpolation)
      - [Derivation](#derivation-1)
      - [Pseudo Code](#pseudo-code-1)
    - [Bicubic Interpolation](#bicubic-interpolation)
      - [Derivation](#derivation-2)
      - [Pseudo Code](#pseudo-code-2)
  - [Analysis](#analysis)
    - [Brief Results](#brief-results)
    - [Nearest Neighbor Interpolation](#nearest-neighbor-interpolation-1)
    - [Bilinear Interpolation](#bilinear-interpolation-1)
    - [Time Complexity Analysis](#time-complexity-analysis)
      - [Enlarge](#enlarge)
      - [Shrunk](#shrunk)
  - [Reference](#reference)

## Objectives

The task of this lab homework is to understand and accomplish codes design for *nearest neighbor interpolation, bilinear interpolation and bicubic interpolation* in python. The specific implementation of these algorithms is packed in corresponding `.py` files, the report and test codes are embedded in the `.ipynb` file. The report contains the derivations, principles and Pseudo codes of the algorithms mentioned above, and then given some optimization, extension and analysis of the results.

Image Interpolation is a significant issue in DIP, we need it when resizing or distorting images from one pixel grid to another. Therefore, the effect and time consumed by varied interpolation algorithms are extraordinarily important. **However, There is always trade-off between efficiency and effect**.

## Principle

### Geometric Center Alignment

Actually, during interpolation we view pixel positions not as integer, but as float values, this understanding helps when implementing those interpolation algorithms. The meaning of geometric center alignment is that the original figure and the new figure should be aligned based on the image center, not the left side. To achieve this, a coordinate transform is essential, here is an example as the figure shows (sampling from 4 to 5):

$$
transform factor \ \alpha=\frac{src size}{dst size} \\
src=(dst+0.5)\times\alpha-0.5
$$
If I want to find the position of A' in float, or find the index of its neighbors. Here is the calculation:

$$
\alpha=\frac{5}{4} \\
A=(dst+0.5)\times\alpha \\
idx_{left}=floor(A-0.5) \\
idx_{right}=ceil(A-0.5)
$$


<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_figure1.jpeg" height="175"></center><center>fig-1 example of center alignment</center>

### Nearest Neighbor Interpolation

#### Derivation

Nearest interpolation is a very simple interpolation method. For a new point of the resized figure, its value is the same with the nearest point of the original figure. The approach we find this nearest point is by using `round` operation after calculate the position of the new point in the original coordinate(multiply a factor of $\frac{original dimension}{new dimension}$). Note that before all these operations, we need to transform the indices for center alignment.

For example, the following *fig-2* shows an original figure of size 2 x 2, we want to enlarge it to size 3 x 3. Assume $(x, y)$ is a point of the resized figure, then its position in the original frame is $(2x/3, 2x/3)$. The result often is a float vector, then round it to integer, e.g., $(1, 2) \to (0.67, 1.33) \to (1, 1)$. Shrunk is similar with enlarging.

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_figure2.jpeg" height="300"></center><center>fig-2 example of nearest neighbor</center>

#### Pseudo Code

```pseudocode
// nearest_11910206
begin with parameters input_file, [h_new, w_new]

    // get input array from filename or just array
    error handling
    array input_raw

    // get resize factor, the \alpha mentioned above
    float h_fac, w_fac
    compute h_fac = h_raw / h_new
    compute w_fac = w_raw / w_new

    // get bias values for center alignment
    array interpolated
    bias float h_bias, w_bias
    compute h_bias = 0.5 * h_fac - 0.5
    compute w_bias = 0.5 * w_fac - 0.5

    // two `for` loops to iterate all items in array interpolated
    for index i
        for index j

            // get the nearest neighbor's index [h_idx, w_idx]
            integer h_idx, w_idx
            compute h_idx = round(h_bias + h_fac * i)
            compute w_idx = round(w_bias + w_fac * j)
            update interpolated[i, j]

    return interpolated
end
```

### Bilinear Interpolation

#### Derivation

**Using repeated linear interpolation:**[^1]

First consider a linear interpolation example in 1-D, like the following figure. The value of f(x) can be expressed by the two neighbor points: $f(x)=\frac{x_2-x}{x_2-x_1}f(x_1)+\frac{x-x_1}{x_2-x_1}f(x_2)$. Therefore, f(x) can be seen as a weighted average of f(x_1) and f(x_2). **Significantly, the border condition of bilinear interpolation can be regarded as linear condition during implementation**. Besides, $x_2-x_1$ normally equal to one in image interpolation because the operation is down pixel by pixel.

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_figure4.jpeg" height="150"></center><center>fig-3 linear interpolation</center>

Then, extend the conclusion to 2-D. Actually, bilinear interpolation is not linear in the whole process but quadratic in the sample location *P*, it could be expressed in a bilinear polynomial form: $f(x,y)=a_{00}+a_{10}x+a_{01}y+a_{11}xy$. The basic derivation is by repeat linear interpolation twice. As shown in the figure below, first sample along x-axis:

$$
\begin{equation}
\begin{aligned}
f(x,y_1) & =\frac{x_2-x}{x_2-x_1}f(Q_1)+\frac{x-x_1}{x_2-x_1}f(Q_2) \\
         & =(x_2-x)f(Q_1)+(x-x_1)f(Q_2) \\
f(x,y_2) & =\frac{x_2-x}{x_2-x_1}f(Q_3)+\frac{x-x_1}{x_2-x_1}f(Q_4) \\
         & =(x_2-x)f(Q_3)+(x-x_1)f(Q_4)
\end{aligned}
\end{equation}
$$
Then sample along y-axis (the sequence of sampling along x and y axes can exchange), writing the equation of f(x, y) in matrix form:

$$
\begin{equation}
\begin{aligned}
f(x,y) & =\frac{y_2-y}{y_2-y_1}f(x,y_1)+\frac{y-y_1}{y_2-y_1}f(x,y_2) \\
       & =\frac{y_2-y}{y_2-y_1}[(x_2-x)f(Q_1)+(x-x_1)f(Q_2)]+\frac{y-y_1}{y_2-y_1}[(x_2-x)f(Q_3)+(x-x_1)f(Q_4)] \\
       & =\begin{bmatrix}
          x_2-x & x-x_1
          \end{bmatrix}
          \begin{bmatrix}
          f(Q_3) & f(Q_1) \\ f(Q_4) & f(Q_2)
          \end{bmatrix}
          \begin{bmatrix}
          y_2-y \\ y-y_1
          \end{bmatrix}
\end{aligned}
\end{equation}
$$
The points lie in the margin of the **enlarged** figure can be dealt with separately, because it only has 3 or 1 (in the corner) neighbors. Therefore, I do linear interpolation for the points in the margin.

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_figure5.jpeg" height="225"></center><center>fig-4 bilinear interpolation</center>

**Using Polynomial to fit:**

As mentioned above, f(x, y) could be written as a multilinear polynomial, therefore using the values of the 4 neighbor points, we can get:
$$
\begin{align}
f(x, y) & \approx a_{00}+a_{10}x+a_{01}y+a_{11}xy \\
        & \Rightarrow [f(Q_3) \ f(Q_1) \ f(Q_4) \ f(Q_2)]^T \\
        \\
\begin{pmatrix}
f(Q_3) \\ f(Q_1) \\ f(Q_4) \\ f(Q_2)
\end{pmatrix} & = 
\begin{pmatrix}
1 & x_1 & y_1 & x_1y_1 \\
1 & x_1 & y_2 & x_1y_2 \\
1 & x_2 & y_1 & x_2y_1 \\
1 & x_2 & y_2 & x_2y_2 \\
\end{pmatrix}
\begin{pmatrix}
a_{00} \\ a_{10} \\ a_{01} \\ a_{11}
\end{pmatrix} \\
\\
\begin{pmatrix}
a_{00} \\ a_{10} \\ a_{01} \\ a_{11}
\end{pmatrix} & = \frac{1}{(x_2-x_1)(y_2-y_1)}
\begin{pmatrix}
x_2y_2 & -x_2y_1 & -x_1y_2 & x_1y_1 \\
-y_2 & y_1 & y_2 & -y_1 \\
-x_2 & x_2 & x_1 & -x_1 \\
1 & -1 & -1 & 1 \\
\end{pmatrix}
\begin{pmatrix}
f(Q_3) \\ f(Q_1) \\ f(Q_4) \\ f(Q_2)
\end{pmatrix} \\
\\
              & =
\begin{pmatrix}
x_2y_2 & -x_2y_1 & -x_1y_2 & x_1y_1 \\
-y_2 & y_1 & y_2 & -y_1 \\
-x_2 & x_2 & x_1 & -x_1 \\
1 & -1 & -1 & 1 \\
\end{pmatrix}
\begin{pmatrix}
f(Q_3) \\ f(Q_1) \\ f(Q_4) \\ f(Q_2)
\end{pmatrix} \\
\\
f(x,y) & = 
\begin{pmatrix}
1 & x & y & xy
\end{pmatrix}
\begin{pmatrix}
x_2y_2 & -x_2y_1 & -x_1y_2 & x_1y_1 \\
-y_2 & y_1 & y_2 & -y_1 \\
-x_2 & x_2 & x_1 & -x_1 \\
1 & -1 & -1 & 1 \\
\end{pmatrix}
\begin{pmatrix}
f(Q_3) \\ f(Q_1) \\ f(Q_4) \\ f(Q_2)
\end{pmatrix} \\

\end{align}
$$
**Using Weighted Mean**

In another view, as mentioned we can see the interpolation as weighted average over the 4 neighbor values, therefore we can a vector $w$ to denote the weights.
$$
\begin{align}
f(x, y) & \approx w_{1}f(Q_{1})+w_{2}f(Q_{2})+w_{3}f(Q_{3})+w_{4}f(Q_{4}) \\
        & =
\begin{pmatrix}
f(Q_3) & f(Q_1) & f(Q_4) & f(Q_2)
\end{pmatrix}
\begin{pmatrix}
w_3 \\ w_1 \\ w_4 \\ w_2
\end{pmatrix}
\end{align}
$$
 Substitute the knowledge of the former polynomial principle, we can get the following result. The weights must add up to 1 for different order of terms. Then extract the weights by do inversing, we get a new matrix form for bilinear interpolation.
$$
\begin{align}
\begin{pmatrix}
1 \\ x \\ y \\ xy
\end{pmatrix}
 & =
\begin{pmatrix}
1 & 1 & 1 & 1 \\
x_1 & x_1 & x_2 & x_2 \\
y_1 & y_2 & y_1 & y_2 \\
x_1y_1 & x_1y_2 & x_2y_1 & x_2y_2
\end{pmatrix}
\begin{pmatrix}
w_3 \\ w_1 \\ w_4 \\ w_2
\end{pmatrix} \\
\\
f(x,y) & =
\begin{pmatrix}
f(Q_3) & f(Q_1) & f(Q_4) & f(Q_2)
\end{pmatrix}
\begin{pmatrix}
w_3 \\ w_1 \\ w_4 \\ w_2
\end{pmatrix} \\ 
& = \frac{1}{(x_2-x_1)(y_2-y_1)}
\begin{pmatrix}
f(Q_3) & f(Q_1) & f(Q_4) & f(Q_2)
\end{pmatrix}
\begin{pmatrix}
x_2y_2 & -y_2 & -x_2 & 1 \\
-x_2y_1 & y_1 & x_2 & -1 \\
-x_1y_2 & y_2 & x_1 & -1 \\
x_1y_1 & -y_1 & -x_1 & 1
\end{pmatrix}
\begin{pmatrix}
1 \\ x \\ y \\ xy
\end{pmatrix} \\
& =
\begin{pmatrix}
f(Q_3) & f(Q_1) & f(Q_4) & f(Q_2)
\end{pmatrix}
\begin{pmatrix}
x_2y_2 & -y_2 & -x_2 & 1 \\
-x_2y_1 & y_1 & x_2 & -1 \\
-x_1y_2 & y_2 & x_1 & -1 \\
x_1y_1 & -y_1 & -x_1 & 1
\end{pmatrix}
\begin{pmatrix}
1 \\ x \\ y \\ xy
\end{pmatrix}
\end{align}
$$
However, it is easy to discover that this matrix form has strong similarity with the one derived from polynomial fitting. In my intuition this methods have the same time complexity with the last one,  therefore I do not implement this method to codes.

#### Pseudo Code

```pseudocode
// bilinear_11910206
begin with parameters input_file, [h_new, w_new]

    // get input array from filename or just array
    error handling
    array input_raw

    // get resize factor, the \alpha mentioned above
    float h_fac, w_fac
    compute h_fac = h_raw / h_new
    compute w_fac = w_raw / w_new

    // get bias values for center alignment
    array interpolated
    bias float h_bias, w_bias
    compute h_bias = 0.5 * h_fac - 0.5
    compute w_bias = 0.5 * w_fac - 0.5

    // get the indexes that represent margins
    integer h_max, w_max, h_margin, w_margin
    compute h_max = h_raw - 1
    compute w_raw = w_raw - 1
    compute h_margin = floor(0.5 / h_fac + 0.5)
    compute h_margin = floor(0.5 / w_fac + 0.5)

    // assign values for the 4 corners
    interpolated[left-top] = input_raw[0, 0]
    interpolated[right-top] = input_raw[0, w_raw]
    interpolated[left-down] = input_raw[h_max, 0]
    interpolated[right-down] = input_raw[h_max, w_raw]

    // assign values for the 4 borderline margins
    for index j

        // handle 2 horizontal borderline margins
        float y
        integer y1, y2
        compute y = w_bias + w_fac * j
        compute y1 = floor(y)
        compute y2 = ceil(y)

        // do linear intepolation in y direction
        interpolated[left-border] = (y2 - y) * input_raw[0, y1] + (y - y1) * input_raw[0, y2]
        interpolated[right-border] = (y2 - y) * input_raw[h_max, y1] + (y - y1) * input_raw[h_max, y2]

    for index i

        // handle 2 vertical borderline margins
        float x
        integer x1, x2
        compute x = h_bias + h_fac * i
        compute x1 = floor(x)
        compute x2 = ceil(x)

        // do linear intepolation in x direction
        interpolated[up-border] = (x2 - x) * input_raw[x1, 0] + (x - x1) * input_raw[x2, 0]
        interpolated[down-border] = (x2 - x) * input_raw[x1, w_max] + (x - x1) * input_raw[x2, x_max]

    // embedded 2 `for` loops to iterate all items in the center part
    for index i exclude margin
        for index j exclude margin
            float x, y
            integer x1, y1, x2, y2
            compute x = h_bias + h_fac * i
            compute y = w_bias + w_fac * j
            compute x1 = floor(x)
            compute y1 = floor(y)
            compute x2 = ceil(x)
            compute y2 = ceil(y)

            update interpolated[i, j]
            compute f(x, y) // equations are given above for different methods

    return interpolated
end
```

### Bicubic Interpolation

#### Derivation

According to the paper in IEEE,  I learn this convolution method for bicubic interpolation (there are other approaches).[^3] The strategy is like the polynomial and weight method of bilinear interpolation, but this time we have 16 coefficients rather than 4. The general function is:
$$
\sum^{3}_{i=0}\sum^{3}_{j=0}a_{ij}x^iy^j
$$
The crucial objective is to solve the $a_{ij}$ coefficients. The paper introduces a BiCubic function:
$$
\begin{align}
W(x) & =\left\{
\begin{aligned}
& (a+2)|x|^3-(a+3)|x|^2 +1 &     & {for \ |x|\leqslant1} \\
& a|x|^3-5a|x|^2+8a|x|-4a &     & {for \ 1<|x|<2} \\
& 0 &     & {otherwise} 
\end{aligned}
\right. \\
a & = -0.5 \ or \ -0.75
\end{align}
$$
Let $0<x<1$, therefore $1<x+1<2$, $-1<x-1<0$, $-2<x-2<-1$, then we substitute to the 4 conditions to $W(x)$, we could get corresponding equations. Substitute to the $x_1\to x_4$, and $y_1\to y_4$ we get two 1 x 4 vectors $\{w_x, w_y\}$. The final result could be:
$$
\begin{align}
f(x,y)=
\begin{pmatrix}
w_{x1} & w_{x2} & w_{x3} & w_{x4}
\end{pmatrix}
\begin{pmatrix}
Q_{11} & Q_{12} & Q_{13} & Q_{14} \\
Q_{21} & Q_{22} & Q_{23} & Q_{24} \\
Q_{31} & Q_{32} & Q_{33} & Q_{34} \\
Q_{41} & Q_{42} & Q_{43} & Q_{44} \\
\end{pmatrix}
\begin{pmatrix}
w_{y1} \\ w_{y2} \\ w_{y3} \\ w_{y4}
\end{pmatrix}
\end{align}
$$
Because of time limit, I am still debugging this algorithm..., therefore I use `scipy` to accomplish it.

#### Pseudo Code

I implement this by using `scipy`, according to the reference.[^2]

## Analysis

Here I import some 3rd-party libraries permitted by teacher, and the `xxx_11910206` files are solutions of this homework:

1. `cv2`: the python-OpenCV package, used for reading images and comparison
2. `numpy`: high efficiency calculating tool, written by C/C++ (using CPU)
3. `matplotlib`: built-in image processing package, used for showing visualization of results
4. `xxx_11910206`: self implemented algorithms
4. `scipy`: contains many scientific math algorithms, like interpolation

I use two other `ndarray test` and `ndarray test_3` for testing my algorithms, the reasons are listed below. Then I set `np.random.seed(0)` in order to control the result of random generated tests. The "seed" would help to make the results of my `ipynb` file repeatable:

1. The size of the given image is a square, but my codes support rectangular input, therefore I would like to use a new test for showing the generalization capability. Besides, I want to show that my algorithms can handle RGB images as well.
2. The pixel image could better depict the difference of different algorithms, it could be helpful for analyzing. The change in visualization is much more obvious. However, I will still use the given figure for time complexity testing.

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

from nearest_11910206 import nearest_11910206
from bilinear_11910206 import bilinear_11910206
from bicubic_11910206 import bicubic_11910206

%matplotlib inline

np.random.seed(0)  # repeatable
test = np.uint8(np.random.randint(0, 255, size=(5, 7)))
test_3 = np.uint8(np.random.randint(0,255,size=(5,5,3)))
raw_gray = cv2.cvtColor(cv2.imread('rice.tif'), cv2.COLOR_BGR2GRAY)
```

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_11910206_3_0.png" alt="png"  /></center>

​    


### Brief Results

Here is all the results that required of this homework. 

**Nearest Neighbor Interpolation**: According to analysis and the efficiency test in the last part, this is the fastest algorithms. The pay-off is that it would occur discontinuity and obvious serration.

**Bilinear Interpolation**: It is more complex than Nearest Neighbor, but it do not have serration for the result gray image. Basically, the result is smooth and continuous, but this method would filter some high-frequency component, thus the image might be a little faintness.

**Bicubic Interpolation**: The time complexity is the greatest, but the interpolation effect is the best. It is important to choose a proper weight policy, exactly choosing an appropriate kernel. The kernel value is usually set to -0.5 or -0.75 (OpenCV set as -0.75).

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_11910206_6_0.png" alt="png" style="zoom:80%;" /></center>


### Nearest Neighbor Interpolation

Comparing the result of OpenCV with self-implemented, they are the same when enlarging. Besides, the result shows that I can apply different resized factors in x and y axes.

During enlarging the figure, nearest neighbor algorithm cannot interpolate smoothly among the original pixels, the boundaries of color blocks is significantly clear.

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_11910206_8_0.png" alt="png"  /></center>

The results of OpenCV and self-implemented algorithms differ when operating shrunk, I look through the code of OpenCV and find that it uses `cvFloor` , which cutoff the integer part of a float number while I use `round` to get the neighbors, thus the down-sample result of OpenCV would lean to the left and top sides while mine is center aligned. The comparison of pixel values are also provided below:

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_11910206_9_0.png" alt="png"  /></center>

```yaml
Raw:
 [[172  47 117 192  67 251 195]
 [103   9 211  21 242  36  87]
 [ 70 216  88 140  58 193 230]
 [ 39  87 174  88  81 165  25]
 [ 77  72   9 148 115 208 243]]
OpenCV:
 [[172 117  67]
 [ 70  88  58]]
Mine:
 [[  9  21  36]
 [ 87  88 165]]
```


I extend my codes for RGB images, actually, this is nearly the same as operating gray images, what's new is to do interpolation separately in 3 color channels. I use the following code to judge what shape of array should be returned: `interpolated = np.zeros(dim, dtype=int) if input_raw.ndim == 2 else np.zeros((dim[0], dim[1], 3), dtype=int)`. When updating the returned array `interpolated`, use the convenient numpy operator `:` (numpy is much more efficient than raw python codes), the RGB channels could be calculated within one line of code:

```python
if input_raw.ndim == 2:
    interpolated[i, j] = input_raw[r_idx, c_idx] # calculate gray figure
else:
    interpolated[i, j, :] = input_raw[r_idx, c_idx, :] # calculate RGB figure
```

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_11910206_11_0.png" alt="png"  /></center>

### Bilinear Interpolation

Below is to sample the "Random Raw" to 100 x 100, the result is similar with OpenCV. The figure with title "Self-linear2" uses repeated linear interpolation, and the one with "Self-polyfit" uses polynomial fit.

It also supports RGB figures just like `nearest_11910206` does. From the results, we could see that bilinear interpolation has better effect than nearest neighbor, it could compensate some transitional values between the original color blocks.

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_11910206_13_0.png" alt="png"  /></center>
<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/interpolation_11910206_14_0.png" alt="png" style="zoom:100%;" /></center>

From the figure above with title "Inverse-Shrunk", it is down-sampled back to 5 x 5 from the image up-sampled to 100 x 100. It reveal that the bilinear process dramatically could be inverse! From wiki, I get the following proof for Inverse computation under special condition (if the point is inside any convex quadrilateral, which means 4-border-polygons that are convex, the "unit square coordinates" could be found).[^1]

The $\{a, b, c, d\}$ could be seen as weights of current interpolation, the unit square are parameterized by $\{\lambda,\mu\}\in[0, 1]$ . The target is to solve these two parameters.
$$
\begin{align}
& a + b\lambda+c\mu+d\lambda\mu=0 \\
\\
& a = x_{00} - x \\
& b = x_{10} - x_{00} \\
& c = x_{01} - x_{00} \\
& d = x_{11} - x_{01} - x_{10} + x_{00} \\
\end{align}
$$
Take 2-d cross product of the system, reveals that:
$$
\begin{align}
& (a+b\lambda+c\mu)\times d & = 0 \\
& (a+b\lambda)\times (c+d\mu) & = 0 \\
& (a+c\mu)\times (b+d\mu) & = 0 \\
& \Rightarrow \\
& C+E\lambda+F\mu & = 0 \\
& B+(C+D)\lambda +E\lambda^2 & = 0 \\
& A+(C-D)\mu+F\mu^2 & = 0 \\
\\
& with \\
& A=a\times b \quad B=a\times c \quad C=a\times d \\
& D=b\times c \quad E=b\times d \quad F=c\times d
\end{align}
$$
Use quadratic formula to solve the equations, we get:
$$
\mathbb{D}=(C+D)^2-4EB=(C-D)^2-4FA \\
\Rightarrow \quad \lambda=\frac{-C-D\pm \sqrt{\mathbb{D}}}{2E} \quad \mu=\frac{-C+D\pm \sqrt{\mathbb{D}}}{2F}
$$
This might explain the dramatic inverse property I found, actually I not sure I totally understand it...

### Time Complexity Analysis

#### Enlarge

I use the built-in `time` package in python to record running time in float seconds, and then use `matplotlib` to plot them, here shows the results. The time complexity of bilinear interpolation and nearest neighbor interpolation are both $O(N^2)$, due to the embedded two for loops. Apparently, bilinear cost more time than nearest neighbor, because it does more calculation in the for loops, which also means that bilinear interpolation has larger coefficient for the 2nd-order term. 

Compare the two bilinear methods, it turns out that when interpolated size is under 800 they hardly have difference. Therefore, it is reasonable to guess that using repeated linear interpolation and polynomial fitting occupy similar calculation.

OpenCV test is weird, I guess it might have down different optimization strategies for these 3 methods. By the way, when interpolated size is larger than 3000, the time cost of nearest neighbor method would increase horribly.

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/buffer_time_result_2.png" alt="png" style="zoom:100%;" /></center>

#### Shrunk

The shrunk result is similar with enlarge, a interesting fact is that shrunk cost much less time than enlarge. This means that the limitation and challenge of interpolation problem is up-sample rather than down-sample. For example, recovering image and super-resolution task might be relevant to this, I guess. 

The OpenCV result is still strange, might relate to its bottom optimization or it use other methods instead.

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/DIP/buffer_time_result_3.png" alt="png" style="zoom:100%;" /></center>

## Reference

[^1]: Bilinear_interpolation. https://en.wikipedia.org/wiki/Bilinear_interpolation.

[^2]: scipy.interpolate.interp2d. https://bbs.huaweicloud.com/blogs/329665.

[^3]: Cubic convolution interpolation for digital image processing