---
title: Qt学习笔记
date: 2022-02-20 22:23:46
tags:
---

- [准备工作](#准备工作)
  - [Qt介绍](#qt介绍)
  - [链接方式](#链接方式)
  - [创建工程](#创建工程)
- [Qt程序设计](#qt程序设计)
  - [Qt主窗口](#qt主窗口)
  - [Qt控件与事件](#qt控件与事件)
    - [QMainWindow和QDialog窗口](#qmainwindow和qdialog窗口)
    - [QLabel文本框](#qlabel文本框)
    - [QPushButton按钮](#qpushbutton按钮)
    - [QLineEdit单行输入框](#qlineedit单行输入框)
    - [QListWidget列表框](#qlistwidget列表框)
    - [QTableWidget表格控件](#qtablewidget表格控件)
    - [QTreeWidget树形控件](#qtreewidget树形控件)
    - [QMessageBox消息对话框](#qmessagebox消息对话框)
  - [Qt信号与槽](#qt信号与槽)
  - [Qt布局管理器](#qt布局管理器)
- [Qt项目案例](#qt项目案例)
  - [ChinaChess项目](#chinachess项目)
  - [自己项目](#自己项目)
- [参考](#参考)

## 准备工作

### Qt介绍

&emsp;&emsp;Qt最初是一个GUI库，用来开发图形界面应用程序，例如WPS、Google地图、YY语音等等，当然最著名的是Linux KDE。现在Qt不断发展，包含了诸如多线程、访问数据库、图像音频处理、网络通信、文件操作等等，已经成为一站式的应用程序开发解决方案。**同时，Qt是Linux环境下C++ GUI开发的事实标准，因此也与嵌入式开发紧密不分。**

&emsp;&emsp;下图是Qt的安装目录和Qt类库的文件目录：

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/others/20220304233538.png" width="650"><center>图 1</center></center>

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/others/20220304233752.png" width="700"><center>图 2</center></center>

&emsp;&emsp;Qt Creator默认Project管理工具用的是qMake，也就是`.pro`文件，由于我用的是CLion，所以默认用的是CMake，当然都是最后生成makefile殊途同归就是了。

&emsp;&emsp;注意看了下网上的博客和讨论，Qt有个大坑是他Debug版本的代码不一定能在Release版本直接使用（有些失误可能Debug版本帮你优化处理了），但是Debug版本的代码效率又很低，所以有人推荐直接使用Release版本。判断是否是Debug版本可以用下面的宏定义：


```c++
#ifdef QT_NO_DEBUG
#define Debug(str)
#else
#define Debug(str) (qDebug() << str)
#endif

qDebug("Debug");
```

### 链接方式

1. **动态链接（Dynamic Link）**：目标程序在运行时需要动态链接库文件（Dynamic Link Library）又叫共享库（Shared Object）。在多个程序运行时，内存中只需要有一份`.dll`或`.so`的动态库，因此提高了内存利用效率；
2. **静态链接（Static Link）**：即在生成目标程序的时候，就将链接库的代码和自己编写的代码都编译链接到一块，链接到静态库的程序通常比较大，但好处是运行时依赖的库文件很少，因为目标程序自己内部集成了很多库代码；

### 创建工程

&emsp;&emsp;Qt对Python的支持好像不错，从字面看用Python应该也能创建各种Application。不知道能不能混合编程，以后实验一下。另外，**Qt Creator 可以根据模板创建多种项目**，这里我直接用Widgets项目来进行学习：
* Qt Widgets Application，支持桌面平台的有图形用户界面（Graphic User Interface，GUI） 界面的应用程序。GUI 的设计完全基于 C++ 语言，采用 Qt 提供的一套 C++ 类库。
* Qt Console Application，控制台应用程序，无 GUI 界面，一般用于学习 C/C++ 语言，只需要简单的输入输出操作时可创建此类项目。
* Qt Quick Application，创建可部署的 Qt Quick 2 应用程序。Qt Quick 是 Qt 支持的一套 GUI 开发架构，其界面设计采用 QML 语言，程序架构采用 C++ 语言。利用 Qt Quick 可以设计非常炫的用户界面，**一般用于移动设备或嵌入式设备上无边框的应用程序的设计**。

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/others/20220306111002.png" width="650"><center>图 1</center></center>

&emsp;&emsp;在项目名称节点下面，分组管理着项目内的各种源文件，几个文件及分组分别为以下几项：

* **`.pro`文件**：项目管理文件，包括一些对项目的设置项
* **Headers分组**：项目内的所有`.h`头文件
* **Sources分组**：项目内的所有`.cpp`源文件。其中，Demo工程创立好后，mainwindow.cpp 是主窗口类的实现文件，与 mainwindow.h 文件对应；main.cpp 是主函数文件，也是应用程序的入口
* **Forms分组**：项目内的所有`.ui`界面文件，界面文件是使用XML语言描述界面组成的文本文件。双击`.ui`文件进入设计模式（实际上是Qt Creator中集成的Qt Designer），能够快速编辑页面样式，如下图所示。

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/others/20220306112541.png" width="650"><center>图 2</center></center>

&emsp;&emsp;在左下角有四个编译运行相关的选项，分别是：选择Debug或Release模式、Run、Debug、Build，这里可以从一开始就使用Release模式进行学习，避免之前提到的模式切换遇到的兼容问题。

## Qt程序设计

### Qt主窗口

&emsp;&emsp;现在自己创建一个新的window类，同样继承自`QMainWindow`，这次我们不使用`.ui`文件来进行设计。Qt有快捷的模板文件创建方式，选择创建`Class`，然后可以选择依赖的组件，自动创建好的`.h`和`.cpp`文件如下：

```c++
#ifndef MYWINDOW_H
#define MYWINDOW_H

#include <QMainWindow>

class MyWindow : public QMainWindow
{
    Q_OBJECT
public:
    explicit MyWindow(QWidget *parent = nullptr);
    // has a default deconstructor
signals:

};

#endif // MYWINDOW_H
```

```c++
#include "mywindow.h"

MyWindow::MyWindow(QWidget *parent)
    : QMainWindow{parent}
{

}
```

&emsp;&emsp;其中，`Q_OBJECT`是一个定义好的宏，所以需要使用“自定义信号与槽”功能的类都要引入这个宏作为成员。在Qt Help中搜索，官方的解释是：“*The Q_OBJECT macro must appear in the private section of a class definition that declares its own signals and slots or that uses other services provided by Qt's meta-object system*”。[^3]

&emsp;&emsp;QWidget是所有组件的基类，借助parent指针，可以为当前窗口指定父窗口。当父窗口被删除时，所有子窗口也会随之一起删除。也可以不指定父窗口（像上面那样指定为`0`或者`nullptr`），那么当前窗口就会作为一个独立的窗口存在。

### Qt控件与事件

&emsp;&emsp;**Qt中的每个控件都由特定的类表示，每个控件类都包含一些常用的属性和方法，所有的控件类都直接或者间接继承自QWidget类。实际开发中，我们可以使用 Qt 提供的这些控件，也可以通过继承某个控件类的方式自定义一个新的控件**。Qt中所有可视化的元素都称为控件，因此之前创建的Window类也是其中之一，称为窗口。

&emsp;&emsp;**Qt事件指的是应用程序和用户或操作系统之间的交互过程，例如用户按下某个按钮、或某个系统的定时任务触发等等**。Qt程序可以接收的事件种类有很多，例如鼠标点击事件、鼠标滚轮事件、键盘输入事件、定时事件等。每接收一个事件，Qt会分派给相应的事件处理函数来处理。所谓事件处理函数，本质就是一个普通的类成员函数，以用户按下某个`QPushButton`按钮为例，Qt会分派给`QPushButton`类中的`mousePressEvent()`函数处理。

&emsp;&emsp;Qt界面程序的`main()`主函数中首先要创建一个`QApplication`类的对象，函数执行结束前还要调用`QApplication`对象的`exec()`函数。一般来说，应用是在`exec()`函数之后才会通过循环接收各种事件。在Help中搜索`int QApplication::exec()`，里面给出的解释如下：

> Enters the main event loop and waits until `exit()` is called. It is necessary to call this function to start event handling. The main event loop receives events from the window system and dispatches these to the application widgets.

#### QMainWindow和QDialog窗口

&emsp;&emsp;窗口一般作为容纳更多其他控件的容器被创建，可以用`QMainWindow`、`QDialog`、`QWidget`三种类来实现。`QWidget`的用法最灵活，既可以作为窗口也可以作为控件使用。**实际开发中，制作应用程序的主窗口可以用`QMainWindow`或者`QWdiget`；制作一个提示信息的对话框就用`QDialog`或`QWidget`；如果暂时无法决定，后续可能作为窗口，也可能作为控件，就选择`QWidget`**。

#### QLabel文本框

#### QPushButton按钮


```c++
MyWindow w;
QPushButton but("Close", &w);
but.setGeometry(10, 10, 100, 50);
QObject::connect(&but, &QPushButton::clicked,&w, &QWidget::close);
w.show();
```

#### QLineEdit单行输入框

#### QListWidget列表框

#### QTableWidget表格控件

#### QTreeWidget树形控件

#### QMessageBox消息对话框

### Qt信号与槽

### Qt布局管理器

## Qt项目案例

### ChinaChess项目

### 自己项目

## 参考

[^1]: Qt快速入门教程系列 Qt Quick介绍. https://wizardforcel.gitbooks.io/qt-beginning/content/61.html.

[^2]: Qt教程. http://c.biancheng.net/view/1817.html.

[^3]: 官方Qt Documentation. https://doc.qt.io/qt-5/qtcore-index.html
