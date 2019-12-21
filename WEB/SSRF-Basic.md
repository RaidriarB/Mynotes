# SSRF

## 前言

网上的教程真的不亲民，好多都看不懂。所以这次想要写一个理解性质，而非总结性质的文章，记录一些学习SSRF的经历。

## 原理

Server-Side Request Forgery  
服务端有一个用来请求资源的方式，用户可以控制这个请求的资源。  
如果用户输入了非预期资源，这个资源没有被过滤，也没有经过访问控制的话，就会请求到非预期的资源。  
原理是很简单的。所以我们的关注点在于： 

1. 获得资源的方法(学习获取资源的函数以及获取资源的协议)
2. 绕过过滤  

## 原理举例

file_get_contents:把文件读入一个字符串中
file_put_contents:把字符串写入到一个文件中

```php
<?php
if (isset($_POST['url'])) {
    $content = file_get_contents($_POST['url']);
    $filename ='./images/'.rand().';img1.jpg';
    file_put_contents($filename, $content);
    echo $_POST['url'];
    $img = "<img src=\"".$filename."\"/>";
}
echo $img;
?>
```

