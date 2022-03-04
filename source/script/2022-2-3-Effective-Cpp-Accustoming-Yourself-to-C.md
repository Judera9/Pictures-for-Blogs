---
title: 《Effective C++ 第三版》1 让自己习惯C++
date: 2022-02-03 12:09:33
categories:
- [学习笔记, Effective C++]
tags:
- C++
- 读书笔记
index_img: /img/default3.png
banner_img: https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/others/index_banner7.jpg
comment: 'valine'
excerpt: ''
---

## 条款01：View C++ as a federation of languages

&emsp;&emsp;当下的C++标准仍然在不断的扩充，我查了一下最新的C++20标准，也有[很多重大的更新](https://www.oschina.net/news/123834/cpp20-published)，比如模块等，这是继C++11以来加入重要新特性的一次更新。在链接下方的评论区有句话说的挺正确：

> C++功能非常多，支持范围非常广，然而各种功能各有各的使用场景。人家支持的全，并不是强行要求你全用，而是按需使用。自己不行，也不愿意学习和了解，还跑出来到处喷。对于c++，一定要清楚你需要什么，能够满足使用即可，而不是一个项目把所有功能都用上，真没必要。你可以先用最基本的功能实现，然后用新特性去改进，从而学习新特性。

&emsp;&emsp;根据本书，C++是一个多重范型编程语言（multiparadigm programming language），同时支持过程形式（procedural）、面向对象形式（object-oriented）、函数形式（functional）、泛型形式（generic）、元编程形式（metaprogramming）。所以C++最大的缺点是它的复杂性，这可能让很多项目变得难以维护。本书对此给出的建议是将C++看作多个次语言来学习和使用（正如上面的评论所说），对于不同的次语言需要考虑不同的高效编程策略，其中主要的四个次语言和其特点如下：

1. C：最基础的部分，特点在于指针（pointers）、数组（arrays）、预处理器（preprocessor）等基础机能，对于程序员要求较高的主要是内存管理、指针运用等，此时pass-by-value通常比pass-by-reference更加高效；
2. Object-Oriented C++：即C with Classes的部分，包括了classes（构造与析构）、封装（encapsulation）、继承（inheritance）、多态（polymorphism）、virtual函数（动态绑定）等；
3. Template C++：这是C++ generic programming的部分，根据本书，template特性带来了TMP（template metaprogramming）的编程范式。不过在C++20特性中，貌似引入了能够替代TMP的新特性；
4. STL：是C++的一个template程序库，有很多现成迭代器和算法可以方便开发；

## 条款02：Prefer consts, enums, and inlines to #define

* 对于单纯变量，最好以const对象或enums替换#defines
* 对于形似函数的macros，最好改用inline函数替换#defines

### const

&emsp;&emsp;使用预处理器不会将被替换的记号名称记入记号表，这可能导致调试时不方便追踪记号名称。除此之外，使用常量可能比宏定义导致更小量的码，从而速度更快。例如：

```cpp
#define ASPECT_RATIO 1.653 // preprocessor
const double AspectRatio = 1.653; // compiler
```

对于常量定义有两种特殊的情况需要注意：

1. 定义constant pointers

&emsp;&emsp;通常对于此类情况，我们希望指针和指针所指向的东西都是const的，因此需要写两次const。通常来说，使用string比char*字符串更好，对于constant pointers的定义更加简洁。例如：

```cpp
// 1st const is constant content ("Scott Meyers")
// 2nd const is constant pointer (authorName)
const char* const authorName = "Scott Meyers";
const std::string authorName("Scott Meyers"); // use `std::string`
```

> **关于`<string.h>`、`<cstring>`、`<string>`的使用**：
> 
> &emsp;&emsp;`<string.h>`是C++标准化（1998年）以前的C++库文件，是原本C风格的字符串库。而`<cstring>`是`<string.h>`在C++标准化之后的对应版本，内容相同并做了一定升级，因此如果需要在C++中使用`<string.h>`，不妨引用`<cstring>`。（大部分原本的C标准库在C++标准化之后都是这么处理的，例如`<cmath>`和`<math.h>`等）这两个库中包含了strcmp、strchr、strstr等char*类型字符串操作的基本函数。
> 
> &emsp;&emsp;`<string>`属于STL（标准模板库）范畴，包含了拟容器`class std::string`的声明（事实上只是`basic_string\<char\>`的typedef），在`<string.h>`的基础上新增了一系列字符串操作。和上述两种global的标准库不同，`<string>`需要使用`std::string s;`来定义string变量。对于内存要求较高的项目，考虑减少使用string，即使在string类中使用了引用计数来减少内存占用。相关内容可以先参考[这篇博客](https://www.jianshu.com/p/6ed6755268f9)，我自己还没有做实验验证其内容。

1. 定义class常量

&emsp;&emsp;需要限制scope在class内，因此将变量声明为class的即static member。需要注意的是，在头文件中我们如下进行的并不是定义，而是声明，因此需要在实现文件中进行定义。该static class变量只能给予一次初值，如果在头文件中不需要使用NumTurns，也可以在实现文件定义式中给予初值。

```cpp
// .h
class GamePlayer {
private:
    static const int NumTurns = 5; // declaration
    int scores[NumTurns]; // use the declared var
    ...
}

// .cpp
const int GamePlayer::NumTurns; // definition
```

### enum hack

&emsp;&emsp;一个属于enumerated type的数值能够权充ints被使用，类似于#define作为一个记号名称，事实上编译器是不会为enum分配内存空间的。枚举类型最常见也最有意义的用处之一就是用来描述状态量，并且增强代码可读性。与const相比，enum变量的地址是无法获取的，因此我们能够用enum来避免别人使用pointer或reference指向我们定义好的整型变量（这一点是const关键字做不到的）。例如：

```cpp
enum Days {
    Mon,
    Tues,
    Wed,
    Thu,
    Fri
};

const int const_Mon = 0;
cout << Mon << endl << const_Mon << endl;
printf("%p\n", &const_Mon);
printf("%p\n", &Mon); // Cannot take the address of an rvalue of type 'Days'
```

### inline

&emsp;&emsp;我们使用预处理器（如宏函数和宏变量等），是因为可以提高程序的运行效率，预处理器会在编译前将这些宏定义以文本方式在代码文件中进行替换，从而避免了在运行时的栈空间占用。但是宏定义纯文本替换带来的诸多限制性，因此使用inline函数是更好的选择。

&emsp;&emsp;inline即内联函数，会在编译阶段**告诉**编译器你要将函数体嵌入到每一个调用该函数的语句块中，这和宏是相似的（但是编译器并不一定听话，聪明的编译器会自己判断是否进行替换）。这么做的好处是能够避免一些小规模函数重复调用带来的堆栈开销，而坏处是可能导致代码膨胀，更多可以参考[这个博客](https://zhuanlan.zhihu.com/p/50812510)。例如下面两种代码，都是用于实现“**以a和b的较大值调用f**”：

```cpp
// macro
#define CALL_WITH_MAX(a, b) f((a) > (b) ? (a) : (b))
// example of limitation
int a = 5;
CALL_WITH_MAX(++a, 0); // ++a run twice
CALL_WITH_MAX(++a, 10); // ++a run once

// inline (better)
template<typename T>
inline void callWithMax(const T& a, const T& b){
    f(a > b ? a : b);
}
```

## 条款03：Use const whenever possible

* 将某些东西声明为const可帮助编译器侦测出错误用法。const可被施加于任何作用域内的对象、函数参数、函数返回类型、成员函数本体。
* 编译器强制实施bitwise constness，但你编写程序时应该使用“概念上的常量性”（conceptual constness）。
* 当const和non-const成员函数有着实质等价的实现时，令non-const版本调用const版本可避免代码重复。

&emsp;&emsp;`const`的用法很多，但是总体来说体现了我们在程序设计时的对编译器强制的语义约束，当我们需要某个变量或者对象不可变更时，加上一个`const`总是更好的选择。**`const`可以用于在classes外部修饰global或namespace作用域的常量，或修饰文件、函数、或block scope中被声明为static的对象。面对指针，你也可以指出指针自身、指针所指物、或两者都（或都不）是const。**

> static 对象在函数中的使用（这个自己还真没用过），其实就是在函数多次调用中并不是将值储存在堆栈中，而是在“全局/静态存储区”。可以参考[这篇博客](https://www.cnblogs.com/chengkeke/p/5417376.html)的例子。

```cpp
// const 用于变量声明时的三种位置
void printInt(int* const pi) // const pointer
void printInt(int const * pi) // const value
void printInt(const int* pi) // const value (same with 2)
```

### STL迭代器

#### 什么是STL迭代器

东西有点多，记在另一篇博客了


### 一般函数声明


### 成员函数声明