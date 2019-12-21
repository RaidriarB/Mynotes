# SQL注入总结-过滤篇

## PHP的一些防御手段

### 1.关闭错误提示 

php.ini中的display_errors=Off

### 2.魔术引号过滤

php.ini里的magic_quotes_gpc=On时，会自动给get/post/cookie（G，P，C）中的单引号（'）、双引号（"）、反斜线（\\）与 NUL字符添加反斜线。  
php.ini里的magic_quote_runtime是给文件中的数据/exec的结果/sql查询中的上述符号添加反斜线。  
PHP5.4之前magic_quotes_gpc默认是on。这之后此特性被废弃，意味着默认是Off。

### 3.addslashes函数

作用和magic_quotes_gpc一样，所以在使用之前应该先检查这个开关是否打开。  

+ 如果magic_quotes_gpc is On，不需要addslashes，如果使用了需要用函数stripslashes去掉。
+ 如果magic_quotes_gpc is Off，必须用addslashes处理，但不需要stripslashes去掉，因为addslashes只是帮助mysql完成SQL的执行，并没有把反斜线存入数据库。

### 4.mysql_real_escape_string函数

转移SQL语句字符串中的特殊字符。  
被转义的字符有：`x00 ' " x1a 空格 换行\n \r`

### 5.htmlspecialchars函数

把预定义的字符转为html实体。  
预定义的字符有：
>& （和号）成为 &amp\; &#38\;  
" （双引号）成为 &quot\; &#34\;  
' （单引号）成为 &apos\; &#39\;  
< （小于）成为 &lt\; &#60\;  
\> （大于）成为 &gt\; &#62\;

### 6.正则表达式替换

自定义正则表达式规则进行过滤。
>preg_match  
preg_match_all()  
preg_replace

### 7.转换数据类型

比如如uid都应该经过intval函数格式为int型

### 8.预编译

这种方式基本能杜绝SQL注入。（存疑）  
实现方式可以使用mysqli的prepare或者PDO。

## 一些绕过的方法

### 1.绕过addslashes【？】

语句：`$id = addslashes($id)`  
绕过方式： 将字符串转为16进制编码数据或使用char函数（十进制）进行转化（因为数据库会自动把16进制转化）  
举例：

```url
?username=0x61646d696e23（admin# –>0x61646d696e23）  
?username=CHAR(97,100, 109, 105, 110, 35)(admin# –>CHAR(97, 100, 109, 105, 110, 35)）  
```

[好用的转码工具](https://evilcos.me/lab/xssor/)  
[字符编码笔记](http://www.ruanyifeng.com/blog/2007/10/ascii_unicode_and_utf-8.html)  
[url编码笔记](http://www.ruanyifeng.com/blog/2010/02/url_encoding.html)  

### 2.绕过strstr

这个函数是区分大小写的，所以可以通过改变大小写来绕过。  
另一个函数`stristr`不区分大小写

### 3.绕过过滤空格

两个方法：  

+ 使用内联注释/**/。举例：`?id=1/**/and/**/1=1`
+ 使用换行符。服务器若为Windows则换行符为%0A%0D，Linux则为%0A。举例：`?id=1%0A%0Dand%0A%0D1=1`

### 4.空字节绕过一些程序外检测

主要因为这些检测常常由原生语言写成，这些语言会把空字节`%00`作为字符串结束的标志。  
只需要在过滤器阻止的字符串前面提供一个采用URL编码的空字节即可。

### 5.构造过滤

有时应用程序采取替换的方式，那么可以让替换过后的字符串变成想要输入的字符串。比如如果替换了select，则可以构造selselectect。

### 6.