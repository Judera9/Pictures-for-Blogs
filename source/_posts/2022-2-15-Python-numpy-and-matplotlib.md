---
title: Python numpy and matplotlib
date: 2022-02-15 23:11:53
math: true
categories:
- 学习笔记
- [课程相关, DIP]
tags:
- DIP
- NumPy
- Matplotlib
index_img: https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/python/20220221145220.png
banner_img: /img/default3.png
comment: 'valine'
---

## Introduction

I adjust this file from the lab tutorial of my DIP course, actually I have used python for more than two semesters, this is not the first time for me to code with python and numpy. So what is the purpose of this blog? I want to record some details of using `numpy` and `matplotlib`, because I sometimes forget some of their usages (like find or remove by index and so on). ~Besides, I would record notes for `pandas` as well.~


```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
```

## Numpy

I refer extensively to [this site](https://www.numpy.org.cn/en/user/quickstart.html#prerequisites) for reviewing `numpy`. The reason why `numpy` is fast and welcome by programmers is because that it uses pre-compiled effective C code and give a convenient vectorized interface for users.

### Primary

* Some basic concepts and attributes of `numpy.ndarray`
* Create numpy arrays for different dimensions
* print arrays

#### What is `numpy.ndarray`

NumPy’s main object is the homogeneous multidimensional array. It is a table of elements(usually numbers), all of the same type, indexed by a tuple of non-negative integers. In NumPy dimensions are called axes. For example, the coordinates of a point in 3D space [1, 2, 1] has one axis. That axis has 3 elements in it, so we say it has a length of 3. In the example codes below, the array `a` has 2 axes. The first axis has a length of 2, the second axis has a length of 3.


```python
a = np.arange(6).reshape(2, 3)
print(a)
```

    [[0 1 2]
     [3 4 5]]



```python
print('ndim', a.ndim)  # count of dimensions (axes)
print('shape', a.shape)  # a tuple of the length of each axes
print('size', a.size)  # count of all elements
print('dtype', a.dtype)  # datatype
```

    ndim 2
    shape (2, 3)
    size 6
    dtype int64


#### How to create `numpy.ndarray`

They could be created from *list, tuple, and built-in useful functions*. Besides, user could use `np.fromfunction` to customize an array with a give function. Here are some function examples:
* array
* zeros, ones, empty
* zeros_like, ones_like, empty_like
* arange, linspace
* fromfunction, fromfile
* random.random


```python
a = np.array([[1, 2, 3], [4, 5, 6]])  # from list
b = np.array([(1, 2, 3), (4, 5, 6)])  # from tuple
c = np.arange(0, 6, 2)  # np.arange(start, stop, step)
d = np.zeros((2, 3))  # create an array of zeros, similar with `c = np.ones((2, 3))`
e = np.zeros_like(
    a)  # create an array of zeros with the same shape and type as a given array, similar with `c = np.ones_like((2, 3))`
print(e)
```

    [[0 0 0]
     [0 0 0]]



```python
def f1(arg_x, arg_y):  # user customized function
    return 10 * arg_x + arg_y


f = np.fromfunction(f1, (5, 4), dtype=int)
f
```




    array([[ 0,  1,  2,  3],
           [10, 11, 12, 13],
           [20, 21, 22, 23],
           [30, 31, 32, 33],
           [40, 41, 42, 43]])



#### Print arrays

* Except for the last axis(printed from left to right), the other dimensions are all printed from top to down.
* Use `set_printoptions` could change the settings of `print()`
* Basic operations and universal functions


```python
# import sys
# np.set_printoptions(threshold=sys.maxsize) # is used to print whole arrays (avoid hiding)
a = np.arange(24).reshape((2, 3, 4))
print(a)
print(np.arange(10000).reshape(100, 100))  # print large matrix
a[1, 2, 3]  # visit the last element
```

    [[[ 0  1  2  3]
      [ 4  5  6  7]
      [ 8  9 10 11]]
    
     [[12 13 14 15]
      [16 17 18 19]
      [20 21 22 23]]]
    [[   0    1    2 ...   97   98   99]
     [ 100  101  102 ...  197  198  199]
     [ 200  201  202 ...  297  298  299]
     ...
     [9700 9701 9702 ... 9797 9798 9799]
     [9800 9801 9802 ... 9897 9898 9899]
     [9900 9901 9902 ... 9997 9998 9999]]





    23



#### Operators and functions

* Support `+`, `-`, `*`, `**`, `+=`, `*=`, and so on, these operators all apply on corresponding single elements.
* Note that `==`, `<`, and `>=` also work, it would return an array of bools.
* Dot product is `@` or `arr1.dot(arr2)`, multiplication by elements is `*`.
* Operating with arrays of different types corresponds to upcasting.


```python
a = np.arange(4)
print(np.sin(a) ** 0.1)  # basic operators
print(a == 2)  # return bools
a.resize(2, 2)  # reshape() return a new array, resize() adjust the original array
print(a @ a)  # dot product
print(a * a)  # element multiply
b = a + 0.1 * np.ones(4).reshape((2, 2)) * 1j
print(b.dtype)  # upcasting to 'float64'
```

    [0.         0.98288773 0.99053676 0.82216476]
    [False False  True False]
    [[ 2  3]
     [ 6 11]]
    [[0 1]
     [4 9]]
    complex128


**Some `ufunc`**:
* There are many universal functions, like `sin`, `cos`, `exp`, they all apply to `ndarray` by elements.
* The universal functions `ufunc` could apply on certain axes when specify them.
* There are many [logic functions](https://numpy.org/devdocs/reference/routines.logic.html), like some `isxxx` functions(`isinf`, `isnan`, and so on), `all` and `any` are also logic functions.
* `apply_along_axis` might be a useful function (?) [refer to this](https://numpy.org/devdocs/reference/generated/numpy.apply_along_axis.html#numpy.apply_along_axis)
* `argmax`, `argsort` is very useful! [refer to this](https://numpy.org/devdocs/reference/generated/numpy.argsort.html#numpy.argsort)
* Some other `ufunc` are listed below in the figure


```python
c = np.arange(12).reshape(3, 4)
print(c.max(axis=1))  # max of each row
print(c.sum(axis=0))  # sum of each column
print(c.cumsum(axis=0))  # cumulative sum along each column
print(np.all(np.array([-1, 4, 5]) == np.array([0, 4, 5])))  # logic function `all`


def f2(arr_arg):
    """Average first and last element of a 1-D array"""
    return (arr_arg[0] + arr_arg[-1]) * 0.5


d = np.array([[7, 8, 9], [1, 2, 3], [4, 5, 6]])
print(d)
print(np.apply_along_axis(f2, 0, d))  # apply along column
print(np.argsort(d, axis=0))  # return the argument of sorted array along columns
```

    [ 3  7 11]
    [12 15 18 21]
    [[ 0  1  2  3]
     [ 4  6  8 10]
     [12 15 18 21]]
    False
    [[7 8 9]
     [1 2 3]
     [4 5 6]]
    [5.5 6.5 7.5]
    [[1 1 1]
     [2 2 2]
     [0 0 0]]


<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/others/20220216231312.png" width="700"></center>

#### Indexing and Slicing


```python
a = np.arange(20).reshape(5, 4)
print(a)  # original
print(a[1, 0])  # indexing, the sequence of start from axis 0
print(a[1:3])  # slicing, missing indices are considered complete slices
print(a[1:3, -1])  # -1 correspond to the last elements
print(a[-1, -1:0:-1])  # the magic form from Dr. Zhang, hahaha~
print(a[..., 0])  # '...' is an alternative for multiple ':'
a[:4:2] = -1  # equivalent to a[0:6:2] = -1; from start to position 4, exclusive, set every 2nd element to -1
print(a)
```

    [[ 0  1  2  3]
     [ 4  5  6  7]
     [ 8  9 10 11]
     [12 13 14 15]
     [16 17 18 19]]
    4
    [[ 4  5  6  7]
     [ 8  9 10 11]]
    [ 7 11]
    [19 18 17]
    [ 0  4  8 12 16]
    [[-1 -1 -1 -1]
     [ 4  5  6  7]
     [-1 -1 -1 -1]
     [12 13 14 15]
     [16 17 18 19]]


### Advanced

#### Change the shape of arrays

* `a.ravel()` return the flattened array, but not change the array itself
* `a.reshape()` return the reshaped array, `a.resize()` change the shape of array


```python
a = np.floor(10 * np.random.random((3, 4)))  # similar with `np.ceil`
print(a)  # range from [0, 10)
print(a.ravel())  # return the flattened array
print(a.reshape(2, 6))  # return the array with modified shape
print(a.T.shape)  # return the transposed array(shape)
```

    [[0. 4. 8. 8.]
     [9. 3. 3. 5.]
     [0. 2. 5. 5.]]
    [0. 4. 8. 8. 9. 3. 3. 5. 0. 2. 5. 5.]
    [[0. 4. 8. 8. 9. 3.]
     [3. 5. 0. 2. 5. 5.]]
    (4, 3)


#### Stacking arrays together
Refer to the tutorial [here](https://www.numpy.org.cn/user/quickstart.html#%E5%B0%86%E4%B8%8D%E5%90%8C%E6%95%B0%E7%BB%84%E5%A0%86%E5%8F%A0%E5%9C%A8%E4%B8%80%E8%B5%B7), besides some concatenate and splitting functions are [here](https://numpy.org/devdocs/reference/generated/numpy.concatenate.html#numpy.concatenate).
* `vstack` vertical appending
* `hstack` horizontal appending
* `column_stack` and `concatenate`also are useful
* `np.c_` translates slice objects to concatenation along the second axis, this is short-hand for `np.r_['-1,2,0', index expression]`, more about `np.r_` is [here](https://numpy.org/devdocs/reference/generated/numpy.r_.html#numpy.r_). The dimension upgrade rule of `np.r_` can refer to [here](https://blog.csdn.net/huhu0769/article/details/52742395).
* `hsplit` and `vsplit` can split arrays


```python
a = np.ones((2, 2))
b = np.zeros((2, 2))
print(np.vstack((a, b)))  # vertical
print(np.hstack((a, b)))  # horizontal
print(np.r_[2:5:5j, 0, [1] * 2, np.array([2,
                                          3])])  # 5j means using np.linspace(start, stop, step, endpoint=1), if not an imaginary number, using np.arange(start, stop, step)
print(np.r_['0,3,2', [1, 2, 3], [4, 5, 6]])  # the last two integers '3, 1' are about dimension upgrading
```

    [[1. 1.]
     [1. 1.]
     [0. 0.]
     [0. 0.]]
    [[1. 1. 0. 0.]
     [1. 1. 0. 0.]]
    [2.   2.75 3.5  4.25 5.   0.   1.   1.   2.   3.  ]
    [[[1 2 3]]
    
     [[4 5 6]]]


#### Copies and Views

When operating and calculating arrays, sometimes the interpreter would copy the data into a new array and return it, sometimes not. **Python is an advanced language, therefore usually it operates by reference, not by value(can be checked by `id()`)**. There are 3 methods of operating `ndarray`, which are `=`, `view` and `copy`.

##### No Copy at All

**Pass by reference, actually is another name of the original array**. This is useful when passing by function parameters, but python interpreter helps us do this, usually we do not do this.


```python
"""No Copy at All"""


def f3(arg_arr):  # pass by reference
    return id(arg_arr)


a = np.arange(4)
b = a  # do assignment '=' by reference(just different names)
b.shape = 2, 2
print(id(a) == f3(a))
print(id(a) == id(b))
```

    True
    True


##### View or Shallow Copy

**This is like the feature of ROI in CV and matrix operation**. This is useful when the matrix data do not need to change when operating. For example, extracting kernel is this kind of operation, slicing itself also returns a *view*.


```python
c = a.view()  # `view` create a new array object share the same data
print(c is a)
print(c.base is a)
c.shape = 4, 1  # c's property could be changed
print(a.shape)  # a's data do not change
print(c.shape)
print(id(a) == id(c))  # this is reference, is shallow copy(like ROI)
a *= 2
print(a)  # a and c both change
del a  # this is like the principle of reference count
print(c)  # c still work
```

    False
    True
    (2, 2)
    (4, 1)
    False
    [[0 2]
     [4 6]]
    [[0]
     [2]
     [4]
     [6]]


##### Deep Copy

**This creat a full copy of the original data**. Sometimes copy should be called after slicing if the original array is not required anymore. For example, suppose a is a huge intermediate result and the final result b only contains a small fraction of a, a deep copy should be made when constructing b with slicing.


```python
d = c.copy()  # a new array object with new data is created
print(d.base is c)  # d doesn't share anything with a

a = np.arange(int(1e8))  # very large array
b = a[:100].copy()  # create a copy and delete
del a  # the memory of ``a`` can be released.
```

    False


#### Common Function API

refer to [here](https://www.numpy.org.cn/reference/routines/)

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/others/20220218211635.png" width="700"></center>

#### Broadcasting

refer to [here](https://www.numpy.org.cn/user/basics/broadcasting.html#%E4%B8%80%E8%88%AC%E5%B9%BF%E6%92%AD%E8%A7%84%E5%88%99), below is one example:


```python
a = np.array([0.0, 10.0, 20.0, 30.0])
b = np.array([1.0, 2.0, 3.0])
print(a[:, np.newaxis] + b)  # `newaxis` insert a new axis, so a become a 4x1 array
```

    [[ 1.  2.  3.]
     [11. 12. 13.]
     [21. 22. 23.]
     [31. 32. 33.]]


#### More about indexing

refer to [here](https://www.numpy.org.cn/user/quickstart.html#%E8%8A%B1%E5%BC%8F%E7%B4%A2%E5%BC%95%E5%92%8C%E7%B4%A2%E5%BC%95%E6%8A%80%E5%B7%A7)

##### Indexing with Arrays of Indices


```python
a = np.arange(12).reshape(3, 4)
print(a)
i = np.array([[0, 1],
              [1, 2]])  # indices for the first dim of a
j = np.array([[2, 1],
              [3, 3]])  # indices for the second dim
print(a[i,j])
l = (i, j) # another way is using a tuple for indexing
print(a[l]) # result is the same
```

    [[ 0  1  2  3]
     [ 4  5  6  7]
     [ 8  9 10 11]]
    [[ 2  5]
     [ 7 11]]
    [[ 2  5]
     [ 7 11]]


* Another usage example is about `argmax`, which is also in the tutorial.
* Use array indices to allocate data is also a good usage.

##### Indexing with Boolean Arrays


```python
a = np.arange(12).reshape(3,4)
print(a[a > 4]) # 1d array with the selected elements
```

    [ 5  6  7  8  9 10 11]


##### ix_() function

refer to [here](https://www.numpy.org.cn/user/quickstart.html#ix-%E5%87%BD%E6%95%B0), it is useful when doing some array operation (?)

## Matplotlib

### Magic in jupyter

I refer to [this site](https://scipy-lectures.org/intro/matplotlib/index.html) for learning `Matplotlib`. There are some magic in Jupyter Notebook, like `%matplotlib inline`, to let user work with `matplotlib` interactively. Use the below code could set which figure formats are enabled(more refer to [this](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-matplotlib)):

```python
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('pdf', 'svg')
```

### Using `pyplot`

`from matplotlib import pyplot as plt` or `import matplotlib.pyplot as plt` might be the first python code in your study. The majority of plotting commands in `pyplot` have Matlab™ analogs with similar arguments. Important commands are explained with interactive examples.

```python
import numpy as np
import matplotlib.pyplot as plt

# Create a figure of size 8x6 inches, 80 dots per inch
plt.figure(figsize=(8, 6), dpi=80)
    
# Create a new subplot from a grid of 1x1
plt.subplot(1, 1, 1)

X = np.linspace(-np.pi, np.pi, 256)
C, S = np.cos(X), np.sin(X)

# Plot cosine with a blue continuous line of width 1 (pixels)
plt.plot(X, C, color="blue", linewidth=1.0, linestyle="-", label="cosine")

# Plot sine with a green continuous line of width 1 (pixels)
plt.plot(X, S, color="green", linewidth=1.0, linestyle="-", label="sine")

# Set x limits
plt.xlim(-4.0, 4.0)

# Set x ticks
plt.xticks(np.linspace(-4, 4, 9))

# Set y limits
plt.ylim(-1.0, 1.0)

# Set y ticks
plt.yticks(np.linspace(-1, 1, 5))

# Save figure using 72 dots per inch
# plt.savefig("exercise_2.png", dpi=72)

plt.legend(loc='upper left')

# Show result on screen
plt.show()
```


```python
ax = plt.gca()  # gca stands for 'get current axis'
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))
```


```python
t = 2 * np.pi / 3
plt.plot([t, t], [0, np.cos(t)], color='blue', linewidth=2.5, linestyle="--")
plt.scatter([t, ], [np.cos(t), ], 50, color='blue')

plt.annotate(r'$cos(\frac{2\pi}{3})=-\frac{1}{2}$',
             xy=(t, np.cos(t)), xycoords='data',
             xytext=(-90, -50), textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

plt.plot([t, t],[0, np.sin(t)], color='red', linewidth=2.5, linestyle="--")
plt.scatter([t, ],[np.sin(t), ], 50, color='red')

plt.annotate(r'$sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
             xy=(t, np.sin(t)), xycoords='data',
             xytext=(+10, +30), textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
```


```python
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(16)
    label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65))
```

{% raw %}

<table border="0" class="docutils">
<colgroup>
<col width="17%" />
<col width="28%" />
<col width="54%" />
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">Argument</th>
<th class="head">Default</th>
<th class="head">Description</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">num</span></code></td>
<td><code class="docutils literal notranslate"><span class="pre">1</span></code></td>
<td>number of figure</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">figsize</span></code></td>
<td><code class="docutils literal notranslate"><span class="pre">figure.figsize</span></code></td>
<td>figure size in inches (width, height)</td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">dpi</span></code></td>
<td><code class="docutils literal notranslate"><span class="pre">figure.dpi</span></code></td>
<td>resolution in dots per inch</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">facecolor</span></code></td>
<td><code class="docutils literal notranslate"><span class="pre">figure.facecolor</span></code></td>
<td>color of the drawing background</td>
</tr>
<tr class="row-even"><td><code class="docutils literal notranslate"><span class="pre">edgecolor</span></code></td>
<td><code class="docutils literal notranslate"><span class="pre">figure.edgecolor</span></code></td>
<td>color of edge around the drawing background</td>
</tr>
<tr class="row-odd"><td><code class="docutils literal notranslate"><span class="pre">frameon</span></code></td>
<td><code class="docutils literal notranslate"><span class="pre">True</span></code></td>
<td>draw figure frame or not</td>
</tr>
</tbody>
</table>

{% endraw %}

{% gi 2 2 %}
<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/python/sphx_glr_plot_linestyles_001.png" height="250"></center>
<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/python/20220221145220.png" height="250"></center>
{% endgi %}
