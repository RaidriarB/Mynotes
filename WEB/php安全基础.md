# php基础知识

### php类型转换机制

php是一种弱类型语言，它支持的类型有：  

> boolean，integer，float，string，array，object，callable，resource，NULL

类型之间转换可能会发生一些有趣的事情，总结如下：  

#### 转化成boolean

""(空字符串),"0"(字符串零),0(整型零),0.0(浮点零),array()(空数组),NULL,尚未被赋值的变量,都会被认为是false。  
任何资源，NAN，-1，都被认为是true。  

#### 字符串转化成数值

如果该字符串没有包含 '.'，'e' 或 'E' 并且其数字值在整型的范围之内（由 PHP_INT_MAX 所定义），该字符串将被当成 integer 来取值，其它所有情况下都被作为 float 来取值。  
字符串的开始部分决定了它的值。  
如果该字符串以合法的数值开始，则使用该数值。否则其值为 0（零）。  
合法数值由可选的正负号，后面跟着一个或多个数字（可能有小数点），再跟着可选的指数部分。指数部分由 'e' 或 'E' 后面跟着一个或多个数字构成。  

### php比较机制

"==="和"!=="即strict比较符,只有在类型相同时才相等。  
"=="和"!="即non-strict比较符。如果比较的两者类型不同，会在类型转换后进行比较：字符串在与数字比较前会自动转换为数字；两个字符串比较，如果两个都是数字形式，则同时转换为数字进行比较。  
一些例子：

```
0 == "a"
"1" == "01"
"100" == "1e2"
"0E32" == "0e21"
```

[php官网给出了"=="比较的一些例子](https://www.php.net/manual/zh/types.comparisons.php)

---

### php伪协议

[php伪协议总结](https://blog.csdn.net/nzjdsds/article/details/82461043)

协议有很多种，比如file://,http://,ftp://等等，但有的协议只在php中得到支持，故称伪协议。  

#### php://

用来访问各个输入输出流。

php.ini中有两个相关的设置

+ allow_url_fopen:默认值是ON，允许url里的封装协议访问文件
+ allow_url_include:默认值是OFF,不允许包含url里的封装协议包含文件

##### php://input

`php://input`代表可以访问请求的原始数据，简单来说POST请求的情况下，php://input可以获取到post的数据。要求`allow_url_include = ON`  

比较特殊的一点，enctype=”multipart/form-data” 的时候 ，php://input 是无效的。  

##### php://filter

常用，任意文件读取，双OFF时可以使用。

用于将读取的数据经过一些过滤器，进行输出。

php://filter 目标使用以下的参数作为它路径的一部分。 一个路径上可以指定很多过滤器，形成一个过滤链。路径是用/作为分隔。

```
resource=<要过滤的数据流>       这个参数是必须的。它指定了你要筛选过滤的数据流。
read=<读链的筛选列表>           该参数可选。可以设定一个或多个过滤器名称，以管道符（|）分隔。
write=<写链的筛选列表>       该参数可选。可以设定一个或多个过滤器名称，以管道符（|）分隔。
<；两个链的筛选列表>           任何没有以 read= 或 write= 作前缀 的筛选器列表会视情况应用于读或写链。
```

举例说明：`php://filter/read=string.rot13/resource=xxx`  是对xxx这个resource进行rot13字母的操作，再输出。

下面是可转伪协议的字串中直接使用的的一些过滤器函数：

+ 字符串过滤器

```
string.rot13
string.toupper
string.tolower
string.strip_tags
```

+ 转换过滤器

```
convert.base64-encode
convert.base64-decode
convert.quoted-printable-encode
convert.quoted-printable-decode
```

> 值得注意的是，resource中的资源仍然可以是php伪协议。例如`php://filter/read=string.rot13/resource=php://filter/read=string.toupper/resource=index.php`
> 
> 利用这个特点，可以迭代地构造过滤链，也可以用于一些bypass。

#### data://

需要双ON的时候才可以使用。  

将用户输入的信息以流的形式传入，需要`allow_url_include = ON`。这个协议并非伪协议，可以参考[» RFC 2397](http://www.faqs.org/rfcs/rfc2397)的格式。  

```
       dataurl    := "data:" [ mediatype ] [ ";base64" ] "," data
       mediatype  := [ type "/" subtype ] *( ";" parameter )
       data       := *urlchar
       parameter  := attribute "=" value
```

在URL中和在代码中的写法不太一样。URL中的写法示例：`data:text/plain;base64,PD9waHAgc3lzdGVtKCJuZXQgdXNlciIpPz4=`，代码中的写法示例：`file_get_contents('data://text/plain;base64,SSBsb3ZlIFBIUAo=')`。

下面举例：  

+ data:text/plain,...

```php
<?php 
　　@include($_GET["file"]);
?>
url: ...?file=data:text/plain,<?php system("net user")?>
result: user information
```

+ data://text/base64,...

```php
<?php 
　　@include($_GET["file"]);
?>
url: ...?file=data:text/plain;base64,PD9waHAgc3lzdGVtKCJuZXQgdXNlciIpPz4=
result: user information
```

+ data://image/jpeg;base64,...

```php
<?php 
　　$jpegimage = imagecreatefromjpeg("data://image/jpeg;base64," . base64_encode($sql_result_array['imagedata'])); 
?>
图片木马 
```

#### phar://及其他压缩协议

这些协议在双off的时候也可以使用。

##### phar://

phar，官网叫做php归档。实际上这是一个用于解压缩的协议，具体使用方法如下：`phar://[待解压缩文件路径+文件名（包含后缀）]/[解压后的文件名称（包含后缀）]`。  

值得注意的是：虽然强制要求必须写上后缀名，但待解压的文件只要文件格式是zip(其他压缩格式有待实验)即可，对后缀名的形式并没有要求。利用这个特性，经常可以进行一些绕过的操作。  

例如：

```
/about.php?file=phar://./images/file.jpg/1.php
[这是把想要上传的php文件打包成了压缩包，又更改成了jpg后缀进行绕过，上传，然后利用phar的解压还原成原来的文件。]
```

##### zip://

zip协议和phar非常类似，只不过它的格式有些差别，并且只能解压zip：`zip://[待解压缩文件路径+文件名.zip]#[解压后的文件名称（包含后缀）]`。在URL中会忽略#号后面的内容，所以要对它进行URL编码：`zip://test.zip%23file.txt`。

##### bzip2://和zlib://

前者只能解压后缀名为`bz2`的bzip2文件，后者只能解压后缀名为`.gz`的文件。用法和上述协议类似，举例如下：  

```
?file=compress.bzip2://[绝对路径]/test.bz2
?file=compress.bzip2://./test.bz2

?file=compress.bzip2://[绝对路径]/test.gz
?file=compress.bzip2://./test.gz
```

这些不常用的协议可以在常用协议被禁止的时候作为备选项。

___

## 反序列化与漏洞

反序列化只是一个特性，真正造成漏洞的是用户可控。通过反序列化这个例子可以体会到一些关于漏洞挖掘的思想。  

序列化：对象转化为字符串。反序列化：带有格式的字符串转化成对象。  

想要序列化，只要写一个php脚本，模拟要序列化的类即可。在反序列化的过程中，会调用一系列的函数。如果能够利用这些函数或者它们调用的函数，找到这个链条上的危险函数，并且变量可控，即可进行攻击。

### 魔术函数

#### 常规

- __construct() 构造函数，对象new（创建）时自动调用

- __destruct() 析构函数，对象销毁时自动调用

- __call()是在对象上下文中调用不可访问的方法时触发  
+ __callStatic()是在静态上下文中调用不可访问的方法时触发  

+ __get()用于从不可访问的属性读取数据  

+ __set()用于将数据写入不可访问的属性  

+ __isset()在不可访问的属性上调用isset()或empty()触发  

+ __unset()在不可访问的属性上使用unset()时触发  

> 对象被销毁的时机：php程序运行结束，或者没有任何变量指向它。  
> 
> [学习链接](https://blog.csdn.net/mizhenxiao/article/details/51922965)

#### __sleep(), __wakeup()

serialize()序列化时，检查类是否有sleep()函数，有则第一个执行。sleep()的预期用途是提交挂起的数据或执行类似的清理任务。 

unserialize()被调用时，首先检查wakeup()函数的存在，若存在则调用。该功能可重构对象具有的任何资源。wakeup()的预期用途是重新建立在序列化期间可能已丢失的任何数据库连接，并执行其他重新初始化任务。  

### 利用

举例：

正常程序逻辑是不会触及class2的，但可以通过反序列化来构造：

```php
<?php
class vulclass {
    var $test;
    function __construct() {
        $this->test = new class1();
    }
    function __destruct() {
        $this->test->action();
    }}

class class1 {
    function action() {
        echo "class1";
    }}

class class2 {
    var $test2;
    function action() {
        eval($this->test2);
    }}

$c = new vulcalss();
unserialize($_GET['test']);
?>
```

可以构造这样的对象，传入参数后就可以执行漏洞函数：

```php
<?php
class vulclass {
    var $test;
    function __construct() {
        $this->test = new ph0en2x();
    }
}
class ph0en2x {
    var $test2 = "phpinfo();";
}
echo serialize(new chybeta());
?>
```

很好的文章  
[第一个](https://www.cnblogs.com/youyoui/p/8610068.html)  
[第二个](https://www.anquanke.com/post/id/84922)

#### 绕过__wakeup()函数

（）自定义反序列化字符串，给出的变量个数小于你定义的个数，就会绕过。

[一个实例](https://blog.boyblog.club/2019/07/08/Week-8-C/)  

#### Auto Loading

unserialize() 函数只能反序列化在当前程序上下文中已经被定义过的类，传统编程需要很多include和require，后来出现了autooading技术，自动导入使用的类。  
还有一个东西要提一下,那就是Composer,这是一个php的包管理工具,同时他还能自动导入所以依赖库中定义的类。这样一来 unserialize() 函数也就能使用所有依赖库中的类了,攻击面又增大不少。

1. Composer配置的依赖库存储在vendor目录下
2. 如果要使用Composer的自动类加载机制,只需要在php文件的开头加上 require **DIR** . '/vendor/autoload.php';
