# 简单技巧
注意，本文需要基本的python语法知识，这些前置知识不会赘述。

## 对切片命名

```python
record = "...123..."
NUM = slice(3,6)#左开右闭
D = slice(0,2)
print(record[NUM][D])
```

## 字符串首位匹配多个选项

这是python为数不多的要求将元组作为参数的函数。

```python
filenames = ["a.py","b.txt","c.cpp"]
patt = (".py",".cpp")
myFile = [f for f in filenames if f.endswith(patt)]
print(myFile)
```

## 字符串连接

这样过于低效。

```python
s = ''
for p in parts:
    s += p
```

建议使用join方法:

```python
data = ["AMCE",12,91.1]
",".join(str(d) for d in data)
# "AMCE,12,91.1"
```

join的这种写法大概考虑到如果每个iterable都实现一个join，比较多余，不如就在字符串这里实现join方法了。

# *号表达式

这个*有点像c语言的指针，用数据结构中对线性表的定义，这样写就明白了  
`head,*tail = [1,2,3,4]`  
`head,*tail = 1,2,3,4`  
结果都是  
`head=1  tail=[2,3,4]`

## 任意长度序列解包

```python
p = (1,2,3,4,5,6)
first,*middle,last = p
#first : 1
#middle : [2,3,4,5]
#last : 6
```

注意：一个表达式中只允许存在一个*号变量，否则：  
`SyntaxError: two starred expressions in assignment`  

## 使用没被使用过的变量对解包后对象进行丢弃

```python
record = ("sam",12,13,102.3,(12,14,2018))
name,*_,(*_,year) = record
#name : sam
# year : 2018
```

# Generator、Iterator和yield

## Iterator

迭代器有next方法的实现，在正确的范围内返回期待的数据以及超出范围后能够抛出StopIteration的错误停止迭代。  
可以直接作用于for循环的数据类型有以下几种：  
一类是集合数据类型，如list,tuple,dict,set,str等  
一类是generator，包括生成器和带yield的generator function  

+ 注意，Iterator和Iterable不一样。  
list、dict、str虽然是Iterable（可迭代对象），却不是Iterator（迭代器）。  
Python的Iterator对象表示的是一个数据流，Iterator对象可以被next()函数调用并不断返回下一个数据，直到没有数据时抛出StopIteration错误。可以把这个数据流看做是一个有序序列，但我们却不能提前知道序列的长度，只能不断通过next()函数实现按需计算下一个数据，所以Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算。  
Iterator甚至可以表示一个无限大的数据流，例如全体自然数。而使用list这样的Iterable对象是永远不可能存储全体自然数的。
+ 文件是可迭代对象，也是迭代器。

## generator

在Python中，这种一边循环一边计算的机制，称为生成器：generator。  
生成器是一个特殊的程序，可以被用作控制循环的迭代行为，python中生成器是迭代器的一种，使用yield返回值函数，每次调用yield会暂停，而可以使用next()函数和send()函数恢复生成器。  
python提供了两种方式建立生成器：  

1. 生成器函数：也是用def定义的，利用关键字yield一次性返回一个结果，阻塞，重新开始  
2. 生成器表达式：返回一个对象，这个对象只有在需要的时候才产生结果  

### 创建generator和使用

+ 生成器表达式：列表生成式的[]改为()即可。  
next(generator)会返回generator的下一个对象，直到最后抛出一个异常  
Generator也是Iterable的，所以可以直接for迭代。  

```python
l = [i for i in range(1,5)]
# [1, 2, 3, 4]
g = (i for i in range(1,5))
# <generator object <genexpr> at 0x10b40f2d0>
next(g)# 1
for i in g:
    print(i)# 2~4
next(g)# Exception
```

```python
Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    next(g)
StopIteration
```

+ 生成器函数：   
具体实现就是把函数实现的返回语句变成yield，这样函数也会变成一个生成器对象。yield语句是返回且暂停，next的时候会继续在上次yield的时候执行。  

```python
def fib():
    a,b = 1,1
    while True:
        yield b
        a,b = b,a+b

f = fib()
for i in range(1,5):
    print(next(f))
#1 2 3 5
```

但是用for循环调用generator时，发现拿不到generator的return语句的返回值。如果拿不到返回值，那么就会报错，所以为了不让报错，就要进行异常处理，拿到返回值，如果想要拿到返回值，必须捕获StopIteration错误，返回值包含在StopIteration的value中

```python
def fib(max):
    n,a,b =0,0,1
    while n < max:
        yield b
        a,b =b,a+b
        n = n+1
    return 'done'#return在生成器中代表生成器的中止，直接报错

g = fib(4)
while True:
    try:
        x = next(g)
        print('generator: ',x)
    except StopIteration as e:
        print("生成器返回值：",e.value)
        break
```

```text
结果：
generator:  1
generator:  1
generator:  2
generator:  3
生成器返回值： done
```

### 来个小例子：从序列中移除重复元素并保持顺序不变

转换成集合的话，顺序可能会改变，所以

```python
def dedupe(items,key=None):
    #key:用来哈希item，如果它本来就可哈希就不需要管了
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)

a = [{'x':1,'y':2},{'x':1,'y':3},{'x':1,'y':2},{'x':2,'y':4}]
print(list(dedupe(a,lambda d:(d['x'],d['y']))))
print(list(dedupe(a,lambda d:d['x'])))
```

```python
[{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
[{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
```
