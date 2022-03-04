---
title: 机器人运动学中表示旋转的方法（四元数、欧拉角、旋转向量）
date: 2022-02-06 19:59:16
math: true
tags:
---

在网上看了一些博客，感觉多数没有把旋转讲明白，包括各种表示法以及转换，因此记录本文整合一下网上相关的介绍，也作为以后复习的参考。

<!--more-->

## 什么是SO3矩阵

### SO3矩阵定义

&emsp;&emsp;最近在复习Robotics运动学和动力学，看的是ETH那份Dynamics讲义，看到运动学旋转矩阵这里的时候想深究一下SO3，讲义上并没有仔细介绍这个概念。简单来说，就是所谓的旋转矩阵群，在机器人学中能够表征刚体围绕原点旋转，并保持被旋转向量的长度和相对矢量方向，同时是线性的；在性质上，是所谓的Special Orthogonal Group，也即正交群（$AA^T=I$）中行列式为1的部分。

### 旋转矩阵


{% katex %}
$$

_{A}r_{AP}=\begin{pmatrix}
_{A}r_{AP_{x}}\\
_{A}r_{AP_{y}}\\
_{A}r_{AP_{z}}\\
\end{pmatrix}\\

_{}r_{AP}=\begin{pmatrix}
_{B}r_{AP_{x}}\\
_{B}r_{AP_{y}}\\
_{B}r_{AP_{z}}\\
\end{pmatrix}\\

\rArr

_{A}r_{AP}=\begin{bmatrix}
_{A}e_{x}^{B} & _{A}e_{y}^{B} & _{A}e_{z}^{B}
\end{bmatrix} \cdot { }_{B}r_{AP}
=C_{AB} \cdot { }_{B}r_{AP}

$$
{% endkatex %}

### 复合旋转矩阵


## 欧拉角（Euler Angle）

### 欧拉角定义


### 几种典型欧拉角及计算



## 李代数基础



### 李群


### 李代数


## 轴线角（Angle Axis）


### 旋转向量


### 与旋转矩阵的转化