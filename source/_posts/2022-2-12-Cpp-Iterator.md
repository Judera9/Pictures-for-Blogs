---
title: STL入门与Iterator失效
date: 2022-02-12 20:43:55
categories:
- [学习笔记]
tags:
- C++
- Iterator
- STL
index_img: https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main/img/2022/others/index_banner7.jpg
banner_img: /img/default7.jpg
comment: 'valine'
excerpt: 简单介绍STL六大组件以及几种不同Iterator的失效情况
---

## STL六大组件

&emsp;&emsp;因为于老师没讲STL，所以补一下课。STL的六大部件是下面这些：容器（Container）、算法（Algorithm）、迭代器（Iterator）、仿函数（Function object）、适配器（Adaptor）、空间配置器（allocator）。[^1]下面分别简单介绍一下：

### 容器 Container

{% raw %}

<table border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="center" width="170">
<center><p>容器</p></center>
</td>
<td valign="center" width="700">
<center><p>特性</p></center>
</td>
<td valign="center" width="130">
<center><p>所在头文件</p></center>
</td>
</tr>
<tr>
<td valign="center" width="170">
<center><p>向量vector</p></center>
</td>
<td valign="center" width="700">
<p>&emsp;&emsp;可以用常数时间访问和修改任意元素，</span>在序列尾部进行插入和删除时，具有常数时间复杂度，对任意项的插入和删除就有的时间复杂度与到末尾的距离成正比，尤其对向量头的添加和删除的代价是惊人的高的</p>
</td>
<td valign="center" width="130">
<center><p>&lt;vector&gt;</p></center>
</td>
</tr>
<tr>
<td valign="center" width="170">
<center><p>双端队列deque</p></center>
</td>
<td valign="center" width="700">
<p>&emsp;&emsp;基本上与向量相同，</span>唯一的不同是，其在序列头部插入和删除操作也具有常量时间复杂度</span></p>
</td>
<td valign="center" width="130">
<center><p>&lt;deque&gt;</p></center>
</td>
</tr>
<tr>
<td valign="center" width="170">
<center><p>表list</p></center>
</td>
<td valign="center" width="700">
<p>&emsp;&emsp;对任意元素的访问与对两端的距离成正比，但对某个位置上插入和删除一个项的花费为常数时间。</span></p>
</td>
<td valign="center" width="130">
<center><p>&lt;list&gt;</p></center>
</td>
</tr>
<tr>
<td valign="center" width="170">
<center><p>队列queue</p></center>
</td>
<td valign="center" width="700">
<p>&emsp;&emsp;插入只可以在尾部进行，删除、检索和修改只允许从头部进行。按照先进先出的原则。</span></p>
</td>
<td valign="center" width="130">
<center><p>&lt;queue&gt;</p></center>
</td>
</tr>
<tr>
<td valign="center" width="170">
<center><p>堆栈stack</p></center>
</td>
<td valign="center" width="700">
<p>&emsp;&emsp;堆栈是项的有限序列，并满足序列中被删除、检索和修改的项只能是最近插入序列的项。即按照后进先出的</span>原则</p>
</td>
<td valign="center" width="130">
<center><p>&lt;stack&gt;</p></center>
</td>
</tr>
<tr>
<td valign="center" width="170">
<center><p>集合set</p></center>
</td>
<td valign="center" width="700">
<p>&emsp;&emsp;由节点组成的红黑树，每个节点都包含着一个元素，节点之间以某种作用于元素对的谓词排列，没有两个不同的元素能够拥有相同的次序，具有快速查找的功能</span>。但是它是以牺牲插入删除操作的效率为代价的</p>
</td>
<td valign="center" width="130">
<center><p>&lt;set&gt;</p></center>
</td>
</tr>
<tr>
<td valign="center" width="170">
<center><p>多重集合multiset</p></center>
</td>
<td valign="center" width="700">
<p>&emsp;&emsp;和集合基本相同，但可以支持重复元素具有快速查找能力</span></p>
</td>
<td valign="center" width="130">
<center><p>&lt;set&gt;</p></center>
</td>
</tr>
<tr>
<td valign="center" width="170">
<center><p>映射map</p></center>
</td>
<td valign="center" width="700">
<p>&emsp;&emsp;由{键，值}对组成的集合，以某种作用于键对上的谓词排列。具有快速查找能力</span></p>
</td>
<td valign="center" width="130">
<center><p>&lt;map&gt;</p></center>
</td>
</tr>
<tr>
<td valign="center" width="170">
<center><p>多重集合multimap</p></center>
</td>
<td valign="center" width="700">
<p>&emsp;&emsp;比起映射，一个键可以对应多了值。具有快速查找能力</span></p>
</td>
<td valign="center" width="130">
<center><p>&lt;map&gt;</p></center>
</td>
</tr>
</tbody>
</table>

{% endraw %}

### 算法 Algorithm

&emsp;&emsp;由头文件`<algorithm>`，`<numeric>`和`<functional>`组成，`<algorithm>`是STL头文件中最大的一个，由一大堆模板函数组成，其中常用到的功能范 围涉及到比较、交换、查找、遍历操作、复制、修改、移除、反转、排序、合并等。。`<numeric>`体积很小，只包括几个在序列上面进行简单数学运算的模板函数，包括加法和乘法在序列上的一些操作。`<functional>`中则定义了一些模板类，用以声明函数对象。[^1]

### 迭代器 Iterator

&emsp;&emsp;实现位于`<itertator>`中，在某种程度上，可以理解为指针来使用。容器适配器 stack 和 queue 没有迭代器，它们包含有一些成员函数，可以用来对元素进行访问。另外，有的Iterator能够使用`++p`，`p++`，`*p`操作，还可以被复制或赋值，以及用`==`和`!=`等比较运算符。具体的每种Iterator的用法是不一样的，需要查手册。一般迭代器都会有对应的常量迭代器，能够避免用户修改指向的内容（类似const void*的指针）。[^3]

<table border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td colspan="3" valign="center">
<p align="center">迭代器功能</p></center>
</td>
</tr>
<tr>
<td valign="center" width="350">
<p>输入迭代器 Input iterator</p>
</td>
<td valign="center" width="350">
<center><p>Reads forward</p></center>
</td>
<td valign="center" width="300">
<center><p>istream</p></center>
</td>
</tr>
<tr>
<td valign="center" width="350">
<p>输出迭代器 Output iterator</p>
</td>
<td valign="center" width="350">
<center><p>Writes forward</p></center>
</td>
<td valign="center" width="300">
<center><p>ostream, inserter</p></center>
</td>
</tr>
<tr>
<td valign="center" width="350">
<p>前向迭代器 Forward iterator</p>
</td>
<td valign="center" width="350">
<center><p>Read and Writes forward</p></center>
</td>
<td valign="center" width="300">
<center><p>&nbsp;</p></center>
</td>
</tr>
<tr>
<td valign="center" width="350">
<p>双向迭代器 Bidirectional iterator</p>
</td>
<td valign="center" width="350">
<center><p>Read and Writes forward and backward</span></p></center>
</td>
<td valign="center" width="300">
<center><p>list, set, multiset, map, mul, timap</span></p></center>
</td>
</tr>
<tr>
<td valign="center" width="350">
<p>随机迭代器 Random access iterator</p>
</td>
<td valign="center" width="350">
<center><p>Read and Write with random access</p></center>
</td>
<td valign="center" width="300">
<center><p>vector, deque, array, string</p></center>
</td>
</tr>
</tbody>
</table>

```cpp
// 举个例子，如何使用Iterator

#include <iostream>
#include <vector>

using namespace std;

int main() {
    vector<int> v{1, 2, 9, 10, 3, 4, 5, 6, 7, 8};
    for (int i = 0; i < v.size(); ++i) // use for loop to iterate
        cout << v[i] << " ";
    cout << endl;

    vector<int>::iterator i; // declare iterator
    for (i = v.begin(); i != v.end(); ++i) // use `i < v.end()` is also fine
        cout << *i << " ";
    cout << endl;
}
```

### 仿函数 Functor

&emsp;&emsp;仿函数(functor)又称之为函数对象（function object），其实就是重载了()操作符的struct或者class，使一个类的使用看上去象一个函数。这些仿函数可以用关联，聚合，依赖的类之间的关系，与用到他们的类组合在一起，这样有利于资源的管理。C语言使用函数指针和回调函数来实现仿函数；在C++里，我们通过在一个类中重载括号运算符的方法使用一个函数对象，而不是一个普通函数。[^2]

```c
// 在C语言中，例如一个用来排序的函数可以这样使用仿函数

#include <stdlib.h>

/* Callback function */
int compare_ints_function(void* A, void* B)
{
    return *((int*)(A)) < *((int*)(B));
}

/* Declaration of C sorting function */
void sort(void* first_item, size_t item_size, void* last_item, int(*cmpfunc)(void*, void*));

int main(void)
{
    int items[]={4, 3, 1, 2};
    sort((void*)(items), sizeof(int), (void*)(items +3), compare_ints_function);
    return 0;
}
```

```cpp
// 在C++中，重载括号运算符实现仿函数

#include <iostream>

using namespace std;

class IsGreaterThanThresholdFunctor {
public:
    explicit IsGreaterThanThresholdFunctor(int t) : threshold(t) {}

    bool operator()(int num) const { // 可以用户design这一部分
        return num > threshold;
    }

private:
    const int threshold; // 利用成员变量的特性，避免全局变量
};

int RecallFunc(int *start, const int *end, IsGreaterThanThresholdFunctor myFunctor) {
    int count = 0;
    for (int *i = start; i != end + 1; i++) {
        count = myFunctor(*i) ? count + 1 : count; // 传参给operator()函数
    }
    return count;
}

int main() {
    int a[5] = {10, 100, 11, 5, 19};
    int result = RecallFunc(a, a + 4, IsGreaterThanThresholdFunctor(10));
    cout << result << endl; // 3
}
```

### 适配器 Adaptor & 空间配置器 Allocator

&emsp;&emsp;适配器是用来修改其他组件接口的STL组件，是带有一个参数的类模板（这个参数是操作的值的数据类型）。STL定义了3种形式的适配器：容器适配器，迭代器适配器，函数适配器。

* **容器适配器**：包括栈（stack）、队列(queue)、优先(priority_queue)。使用容器适配器，stack就可以被实现为基本容器类型（vector,dequeue,list）的适配。可以把stack看作是某种特殊的vctor,deque或者list容器，只是其操作仍然受到stack本身属性的限制。queue和priority_queue与之类似。容器适配器的接口更为简单，只是受限比一般容器要多。

* **迭代器适配器**：修改为某些基本容器定义的迭代器的接口的一种STL组件。反向迭代器和插入迭代器都属于迭代器适配器，迭代器适配器扩展了迭代器的功能。

* **函数适配器**：通过转换或者修改其他函数对象使其功能得到扩展。这一类适配器有否定器（相当于"非"操作）、绑定器、函数指针适配器。函数对象适配器的作用就是使函数转化为函数对象，或是将多参数的函数对象转化为少参数的函数对象。

&emsp;&emsp;STL内存配置器为容器分配并管理内存，统一的内存管理使得STL库的可用性、可移植行、以及效率都有了很大的提升。SGI-STL的空间配置器有2种，一种仅仅对c语言的malloc和free进行了简单的封装，而另一个设计到小块内存的管理等，运用了内存池技术等。在SGI-STL中默认的空间配置器是第二级的配置器。[^1]

## 具体学习Iterator

### 自增操作

&emsp;&emsp;注意`A(i++);`是先执行`A(i)`，再执行`i++;`，后者相反。

```cpp
int i = 1;
    cout << i++ << endl; // 1
    cout << ++i << endl; // 3
```

### 迭代器失效

可以参考[第四个Reference](https://blog.csdn.net/u010318270/article/details/78575371?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_default&utm_relevant_index=2)，讲的很细致。关键的点基本都在下面：[^4]

* C++标准中，**顺序容器的erase函数会返回iterator，但关联容器的erase函数不返回iterator**；
* 对于顺序容器vector、deque，删除当前的iterator会使后面所有元素的iterator都失效。这是因为vector、deque使用了连续分配的内存，删除一个元素导致后面所有的元素会向前移动一个位置。erase方法可以返回下一个有效的iterator；
* 对于关联容器map、set、multimap、multiset，删除当前的iterator，仅仅会使当前的iterator失效，只要在erase时，递增当前iterator即可。这是因为map之类的容器，使用了红黑树来实现，插入、删除一个结点不会对其他结点造成影响；
* 对于顺序容器list，erase方法可以返回下一个有效的iterator。由于list是一个链表，删除当前的iterator，仅仅会使当前的iterator失效，所以也 可以在erase时，递增当前的iterator。
* erase函数返回被删除元素的下一个元素的迭代器。**在STL中，不能以指针来看待迭代器，指针是与内存绑定的，而 迭代器是与容器里的元素绑定的**。

## Reference

[^1]: https://www.cnblogs.com/welen/articles/3533008.html

[^2]: https://blog.csdn.net/K346K346/article/details/82818801

[^3]: http://c.biancheng.net/view/6675.html

[^4]: https://blog.csdn.net/u010318270/article/details/78575371?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_default&utm_relevant_index=2