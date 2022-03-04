---
title: 介绍树莓派Pico | MicroPython插件
date: 2022-02-12 18:18:56
categories:
- [学习笔记, Raspberry Pico]
- [知识科普]
tags:
- Raspberry
- Pico
- MicroPython
- 嵌入式
- Python
- PyCharm
index_img: https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main/img/2022/pico/20220212190432.png
banner_img: https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/others/index_banner7.jpg
comment: 'valine'
excerpt: 树莓派Pico时2021年发布的微型控制器，买来把玩一下。树莓派的品控还是很值得信赖的，虽然相比最大竞争对手ESP32现在Pico还是小菜鸡哈哈哈！
---

## Raspberry Pico

推荐网页：[树莓派 Pico 中文站](https://pico.org.cn/)

> 上面的站点提供了树莓派 Pico 开发板的说明文档，以及完备的 RP2040 芯片资料，本文也有参考上面的内容。

### Pico 规格参数

&emsp;&emsp;这里涉及了很多嵌入式方面的知识，这一块我学的不是很好，有一些看得不是很明白的以后用到再来学吧。看了看相关的评测[^3]，ESP32不仅比Pico便宜而且外设还丰富的多，而且也支持MicroPython。不过我自己也只是买着玩玩，不用在意这些，个人感觉主要树莓派学习门槛更低吧。

- 双核 Arm Cortex-M0 + @ 133MHz
- 芯片内置 264KB SRAM 和 2MB 的板载闪存
- 通过专用 QSPI 总线支持最高 16MB 的片外闪存
- DMA 控制器
- 30 个 GPIO 引脚，其中 4 个可用作模拟输入
- 2 个 UART、2 个 SPI 控制器和 2 个 I2C 控制器
- 16 个 PWM 通道
- USB 1.1 主机和设备支持
- 8 个树莓派可编程 I/O（PIO）状态机，用于自定义外围设备支持
- 支持 UF2 的 USB 大容量存储启动模式，用于拖放式编程

> **SRAM是什么**：SRAM (static RAM) is random access memory (RAM) that retains data bits in its memory as long as power is being supplied. Unlike dynamic RAM (DRAM), which stores bits in cells consisting of a capacitor and a transistor, SRAM does not have to be periodically refreshed. Static RAM provides faster access to data and is more expensive than DRAM. SRAM is used for a computer's cache memory and as part of the random access memory digital-to-analog converter on a video card.[^1]

> **QSPI是什么**：QSPI是Queued SPI的简写，是Motorola公司推出的SPI接口的扩展，比SPI应用更加广泛。在SPI协议的基础上，Motorola公司对其功能进行了增强，增加了队列传输机制，推出了队列串行外围接口协议（即QSPI协议）。片外闪存顾名思义就是外接的Flash存储空间。[^2]

> **PIO是什么**：这是应该是Pico最大的亮点，我没有看得很明白官方的说明。大概就是说能够使用PIO来实现硬件接口，相对于软件模拟的方式，可以达到更高的时钟精度、高得多的I/O吞吐量，还能分担一点CPU的计算工作，比如奇偶校验、和校验等。[^3]

<center>
    <img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main/img/2022/pico/20220212190432.png" width="1000">
    <center>Pico原理图</center>
</center>

### Pico提供的开发工具

&emsp;&emsp;有一个C\C++的SDK，是专门给Pico设计的，感觉没有必要，用这套SDK不如用STM32系列的SDK。除了C++之外还有一个MicroPython的SDK，我是打算用这个来做点小东西，顺便学习一下各种嵌入式常见的外设。除此之外，学一些MicroPython也挺好的，主要看这个文档[Pico Python SDK](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf)。除此之外还有[RP2040 硬件设计](https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf)、[RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)和[树莓派 Pico Datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)这三个文档也可以作为学习过程的参考，主要和RP2040和Pico的硬件外设有关。

## PyCharm MicroPython 插件

&emsp;&emsp;直接在PyCharm的Settings-Plugins中去搜索“MicroPython”插件然后安装，完成后需要在Project中进行配置，在Settings-Languages & Frameworks-MicroPython对开启该插件进行勾选，然后选择对应的Device type和Device path（我是在linux ubuntu下所以是dev/ttyACM0）。完成配置后使用如下程序进行测试，如果LED灯闪烁说明配置成功（REPL显示对应输出）：

```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)
while True:
    led.value(1)
    print("led light on")
    time.sleep(1)

    led.value(0)
    print("led light off")
    time.sleep(1)

```
<center>
    <img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/pico/20220212200558.png" width="600">
    <center>Pico原理图</center>
</center>

## Reference

[^1]: https://whatis.techtarget.com/definition/SRAM-static-random-access-memory

[^2]: https://www.cnblogs.com/firege/p/9435349.html

[^3]: https://www.zhihu.com/question/440677296