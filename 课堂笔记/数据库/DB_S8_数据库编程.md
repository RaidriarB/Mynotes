# 编程

## 嵌入式SQL

SQL提供了两种使用方式：交互式和嵌入式

### 处理方式-预编译

主语言程序（含SQL语句）->RDBMS预处理程序 -> SQL语句转换成函数调用 -> 主语言的编译程序 -> 主语言程序

为了区分SQL语言与主语言，SQL要加上EXEC前缀和分号结束。

例如

```c
//c语言程序
//主变量：用来和sql交互的变量
EXEC SQL BEGIN DECLARE SECTION/*主变量说明 开始*/
char department[64]
int HSage;
EXEC SQL END DECLARE SECTION
long SQLCODE；
EXEC SQL INCLUDE sqlca; //定义sql通信区
```

后面还有很多 很麻烦  现在都不用了

## 存储过程

### PL/SQL

是SQL的扩展，增加了过程化语句的功能。

### 存储过程

PL/SQL块如果作为命名块，编译后优化保存，使用时调用即可，称为存储过程。

创建存储过程

```sql
CREATE Procedure <PROCname> ...
```



### 
