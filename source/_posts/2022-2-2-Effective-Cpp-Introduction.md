---
title: 《Effective C++ 第三版》0 导读
date: 2022-02-02 10:55:41
categories:
- [学习笔记, Effective C++]
tags:
- C++
- 读书笔记
index_img: /img/default3.png
banner_img: https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/others/index_banner7.jpg
comment: 'valine'
excerpt: 本章讲述作者写本书时的一些考量，以及对行文风格等进行了描述。另外讲解了一些术语和概念，我个人进行了一些拓展，可能后面章节作者也会提到这些。
---

## Terminology

### 声明-declaration

在《C++ Primer》中提到：

> 变量声明：用于向程序表明变量的类型和名字。

```Cpp
extern int x; // declare an object
std::size_t numDigits(int number); // declare a function
class Widget; // declare a class

template<typename T> // declare a template
class GraphNode;
```

#### extern关键字

&emsp;&emsp;通过使用extern关键字能够声明变量名而不定义它，使用extern编译器不会给变量分配存储空间。所以`extern int x;`是声明而不是定义，而`int x;`是声明也是定义。但是如果对声明进行了initialization，如`extern int x = 1;`，则一定是定义。

&emsp;&emsp;对函数来说如果加了`{}`就是定义，如果没有就是声明。**在一个程序中，变量或函数可以声明多次（如下会提示`Clang-Tidy: Redundant 'foo' declaration`），但是定义只能有一次**，如下代码能够编译成功：

```cpp
int foo(int a); // declaration
int foo(int a); // redundant declaration
int foo(int a){ // definition
    return 0;
}
```

#### 使用std

&emsp;&emsp;为了方便，作者在后面章节的代码中省略了C++标准程序库的命名空间`std::`的书写，但是在实际编译时是不能省略的。另外，`use namespace std;`并不是一个好选择，因为会引入很多不必要的名称，这可能会导致灾难性的结果。在《C++ Primer Plus》的“第九章-内存模型和名称空间”中，提到：

> &emsp;&emsp;一般说来，使用using命令比 使用using编译命令更安全，这是由于它只导入了制定的名称。如果该名称与局部名称发生冲突，编译器将发出指示。using编译命令导入所有的名称，包括可能并不需要的名称。**如果与局部名称发生冲突，则局部名称将覆盖名称空间版本，而编译器并不会发出警告。**另外，名称空间的开放性意味着名称空间的名称可能分散在多个地方，这使得难以准确知道添加了哪些名称。

#### 为什么使用size_t

&emsp;&emsp;上面提到的标准库中的size_t，是很多C\C++ Programmer知道但是很多时候不敢用的一个typedef的unsigned integer类型。使用size_t能够使得代码更加便于在不同系统间移植（如IP16L32和I16PL32），同时增加移植性和可读性，可以参考给出的链接[Why size_t matters](http://web.archive.org/web/20101209143037/http://www.eetimes.com/discussion/programming-pointers/4026076/Why-size-t-matters?)。

#### 函数签名-signature

&emsp;&emsp;官方定义的C++ signature只包括函数的参数，不包括返回类型。编译器在检查函数signature是否重复时，如果两个函数声明只有返回类型不同，编译器同样会报错，因为它不知道调用的是哪个函数。但是本书为了帮助理解将返回类型视为signature的一部分。

```cpp
int foo(int a);
double foo(int a);
```

&emsp;&emsp;上面的declaration我使用C++14标准会报*“Functions that differ only in their return type cannot be overloaded”*。如下的代码是可以编译通过的（对于C89来说这两种都不行，C只检查函数名，而不会将参数类型和返回值加到signature中）：

```cpp
int foo(int a, int b);
double foo(int a);
```

### 定义-definition

&emsp;&emsp;书中描述是*“definition的任务是提供编译器一些声明式所遗漏的细节“*，个人感觉说的不够清楚。在《C++ Primer》中提到：

> 变量定义：用于为变量分配存储空间，还可为变量指定初始值。程序中，变量有且仅有一个定义（定义也是声明）。

#### 关于声明与定义的程序设计风格

&emsp;&emsp;参考博客[C++定义与声明 区别](https://blog.csdn.net/sjxbf/article/details/6310150)，我觉得有几点很值得注意：

1. 不要把变量定义放入.h文件，这样容易导致重复定义错误。
2. 但是值在编译时就已知的const变量的定义、类的定义、inline 函数的定义可以放到头文件中。
3. 尽量使用static关键字把变量定义限制于该源文件作用域，除非变量被设计成全局的。
4. 可以在头文件中声明一个变量，在用的时候包含这个头文件就声明了这个变量。

### 初始化-initialization

&emsp;&emsp;初始化是“给予对象初值”的过程，通常由构造函数constructor完成。需要注意如下三个特别的构造函数：default构造函数、copy构造函数、以及copy assignment操作符。

#### default构造函数

&emsp;&emsp;default构造函数的要求是*“一个可被调用而不带任何实参者”*，也可以是每个参数都有缺省值。**通常来说，建议构造函数被声明为explicit，这样能够阻止implicit type conversions。**

#### copy构造函数和copy assignment操作符

&emsp;&emsp;copy构造函数被用来*“以同型对象初始化自我对象”*，而copy assignment操作符被用来*“从另一个同型对象中拷贝其值到自我对象”*。copy构造和copy赋值的区别在于是否有新的对象被创建。**这两个都是典型的pass-by-value的方式，而一般更好的方式是pass-by-reference-to-const。**书中的例子如下：

```cpp
class Widget {
public:
    Widget(); // default构造函数
    Widget(const Widget& rhs); // copy构造函数
    Widget& operator=(const Widget& rhs); // copy assignment操作符
    ...
};
Widget w1; // 调用default构造函数
Widget w2(w1); // 调用copy构造函数
w1 = w2; // 调用copy assignment操作符
```

### Standard Template Library-STL

&emsp;&emsp;是C++标准程序库的一部分，内含容器（vector、list、set、map等），迭代器（iterator、set<string>::iterator等），算法（for_each、find、sort等）及其相关机能。作者说STL是非常有用的，不过我基本没用过（因为我C++课的老师主要让我们搞速度优化，用STL肯定卷不过别人了）。

### 不明确行为-undefined behavior

&emsp;&emsp;带有undefined behavior的程序通常是令人崩溃的，这样的程序即使能够编译成功，在执行过程中可能有时正常执行，有时造成崩坏，有时产生不正确的结果。因此，使用C++编程时要能够自己处理异常并小心避免undefined behavior。下面程序的返回值就是一个随机的结果，因为数组name的大小为6，发生了越界。

```cpp
char name[] = "Darla";
char c = name[10];
std::cout << c << std::endl;
```

## TR1和Boost

TR1是描述C++许多新机能的一份规范，而Boost是一个相关的开源平台。关于这方面，下面提供了一些可能有帮助的C++学习相关资源链接。

* [C++ 有用的资源](https://www.runoob.com/cplusplus/cpp-useful-resources.html)
* [C++ Standard Library headers](https://en.cppreference.com/w/cpp/header)
* [C++ Programming（书）](https://en.wikibooks.org/wiki/C++_Programming)
* [C++ FAQ LITE — Frequently Asked Questions](http://www.sunistudio.com/cppfaq/)
* [Free C / C++ Libraries, Source Code and Frameworks](https://www.thefreecountry.com/sourcecode/cpp.shtml)
* [boost](https://www.boost.org/)