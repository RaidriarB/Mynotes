# PHP漏洞总结

## 奇怪的特性

php会把空格和点（.）自动替换成下划线（_）。  

## 弱类型

### 自动转换

```php
判断 "数字值" == "数字值" 字符串自动转换为数字。
！！注意，数字值不能包括十六进制的字符！否则是不能转换成数字的，仍然会根据字符串进行比较。这一点在MD5中有所体现
判断 数值 == "字符串" 字符串自动转换为数字
NULL == False
NULL == ''
```

### strcmp

+ strcmp(string \$str1,string \$str2)

+ str1\<str2返回小于0的数，str1\>str2返回大于0的数，等于返回0

```php
$flag = "flag{...}";
if(strcmp($_GET['flag'],$flag) == 0){
    echo "success. flag:".$flag;
}
```

> payload: flag[ ] = ... --> 返回NULL  -->  NULL==0  -->  Bypass

+ fix: use `===`

### md5

要注意的是，弱类型判断时只有0e后面全为数字，才可以判断双等！

```
"0e12" == "0e23"  TRUE
"0e1c" == "0e12"  FALSE
"0e1c" == "0e2c" ,"0e1c" == "0e1cc" FALSE
这个例子说明，如果md5字串不是全数字的话，比较时候根本不会转换成数字，直接会按照字符串比较
```

如果是`==`

> payload: md5 (array) == NULL
> 
> payload : "0e[0-9]+" == "0e[0-9]+"
> 
> payload: 

如果是`===`

> md5(array1) === md5(array2) === NULL
> 
> md5 collision：[fastcoll](https://github.com/upbit/clone-fastcoll)

```
0e644c2d05e6d81ff04194145d497c74 1aaabw
0e93fcef5a44bbc455bb54011b8c6b2f 2aaady
0edfb3f3a9ab8d5ae227861e9a44b3e7 3aaacO
0eabd2eeb3b01d5b516a4e5bc51d6a43 4aaaci
0e1e066173172fd0eb55ac92ee4d9254 5aaabd
0e98a9e89b8bf419701c85ec8183247c 6aaabp
0e17990dcefa714d524be3fcab79491c 7aaaad
0e5a9f50d8369a2bbbab1797752111f1 8aaalf
0e2eb438bed241fdb0f6fa0d93ac86c5 9aaaaE
```

### switch

+ 如果switch是数字类型的case的判断时，switch会将其中的参数转换为int类型。

```
$i ="1abc";
switch ($i) {
case 1:
    echo "i is 1";
    break;
case 2:
    echo "i is 2";
}
```

会输出 `i is 1`

### in_array、array_search

+ bool in_array ( mixed \$needle , array \$haystack [, bool $strict = FALSE ] )

+ 如果strict参数没有提供，使用`==`判断`$needle`是否在`$haystack`中 

+ strict的值为true时，使用`===`

+ array_search 同理

```php
$array=[0,1,2,&#39;3&#39;];
var_dump(in_array(&#39;abc&#39;, $array));  //true
var_dump(in_array(&#39;1bc&#39;, $array));    //true
```

## Bypass

#### 绕过正则匹配

增加一个+号

场景来源：

```php
if (isset($_GET['var'])) { 
    $var = base64_decode($_GET['var']); 
    if (preg_match('/[oc]:\d+:/i', $var)) { 
        die('stop hacking!'); 
    } else {
        @unserialize($var); 
    } 
```

这个正则表达式检测开头为o或c，接下来是冒号，然后是数字的模式，忽略大小写。使用如下方式可以绕过：`O:+4:"Demo":2:{s:10:"Demofile";s:8:"fl4g.php";}`  

**经过尝试，注意：加号只能在冒号后面添加，其他地方不可以。**  

具体绕过原理不明。  

### is_numeric

### %00截断

> php版本小于等于5.2.9和magic_quotes_gpc关闭，两个条件都必须满足才能截断。

影响的函数

+ include,include_once,require,require_once
+ file_exists
+ ereg,eregi(正则表达式匹配)
+ file_get_contents

不处理截断的函数

+ strlen
