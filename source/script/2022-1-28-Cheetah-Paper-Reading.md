---
title: MIT Cheetah 3 论文阅读笔记
date: 2022-01-28 19:34:38
sticky: 100
tags:
- 控制
- MPC
- Mit Cheetah
- 论文
index_img: https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/mit_cheetah/Cheetah-Paper-Reading-0.png
banner_img: https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/mit_cheetah/index_banner7.jpg
comment: 'valine'
categories:
- [学习笔记, 论文阅读]
math: ture
---

[MIT Cheetah 3: Design and Control of a Robust, Dynamic Quadruped Robot](https://ieeexplore.ieee.org/abstract/document/8593885)

<!--more-->

## Introduction

&emsp;&emsp;这篇paper主要讲了MIT Cheetah 3的设计和控制方面，可以看作是一篇overview性质的文章，关于驱动器方面设计的问题可以参考另一份论文“[A Low Cost Modular Actuator for Dynamic Robots](https://dspace.mit.edu/handle/1721.1/118671)”，应该是Katz, Benjamin G的毕业论文。后面找时间再记录学习和阅读驱动这方面的笔记，这篇中其实涉及驱动不多，所以我主要记录Control方面的东西。

&emsp;&emsp;论文分五个Section：Section I是Introduction，反正就含蓄的装逼一下，提到了ETH的ANYmal（用的是SEA驱动）并做了对比，然后简单介绍了一下论文结构。Section II讲的是Design部分，介绍了硬件平台的设计，主要是腿和驱动的设计。有些指标我目前没什么概念，比如那个gear ratio，这一块打算之后看另外的论文来继续学习。Section III讲的是控制和软件设计......

## Design

[关于驱动，另一篇笔记]()

&emsp;&emsp;关于Locomotion相关的计算和Low-Level Control的设计......

https://blog.csdn.net/Double_qiang/article/details/81222219

## Control

&emsp;&emsp;控制方面整体的设计如图1所示，图中的每一个block都是模块化的（modular）。手柄（operator）给出一个high-level的运动指令，即${\dot{p}_d, \dot{\phi}_d}$

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/mit_cheetah/7A8F697E-25D7-4FDF-9BFF-9B9481D378F2.jpeg" width="750"><center>图 1</center></center>