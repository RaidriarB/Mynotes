# 数据库的完整性

## 概述

完整性包括：  

+ 正确性

+ 相容性

完整性规则，也称完整性约束条件，用有关的语言进行描述，系统加以编译之后，放在数据库中，可以修改删除。  

分类：

+ 实体完整性

+ 参照完整性

+ 用户定义的完整性

## 实体完整性

### 定义

就是Primary Key。在`Create table`时用`Primary Key`定义。可以定义在列上，也可以定义在表上。  

如果主码由多个属性构成，则只能定义在表上。  

默认为PK构造索引，减少检查的开销。

```sql
create table stu(
    sno int,
    
)
```

### 完整性检查

+ 是否唯一

+ 是否为空

不满足条件则会拒绝操作。  

检查PK唯一的机制：

+ 全表扫描

+ 索引（B+ Tree）

## 参照完整性

### 定义

就是Foreign Key。创建表的时候用`Foreign Key`定义哪个是外码，`Reference`定义被参照的主码。  

可以列级也可以表级定义。  

### 完整性检查

FK约束至少关系到两个表，两个表发生改动都可能破坏完整性。  

+ 参照表插入元组——可能破坏被参照表的参照完整性——拒绝

+ 修改参照表FK——可能破坏被参照表的参照完整性——拒绝

+ 删除被参照表元组——可能破坏参照表的参照完整性——拒绝or级联删除or设置为NULL

+ 修改被参照表PK——可能破坏参照表的参照完整性——拒绝or级联删除or设置为NULL

至于选择【拒绝】还是【级联操作】，在定义的时候可以定义【在删除、更新的时候怎么办】的选项。

```sql
create table sc(
sno char(9) NOT NULL,
cno char(4) NOT NULL,
foreign key (sno) references student(sno)
    on DELETE CASCADE
    on UPDATE CASCADE
foreign key (cno) references course(cno)
    on DELETE NO ACTION
)
--NO ACTION就是拒绝
--CASCADE就是级联
--具体根据业务情况设置
```

## 用户定义的完整性

这是针对一些具体的应用，由用户提出的完整性约束。这些要求在定义数据库表的时候得到实现，就不需要程序来承担了。  

转移到底层的好处是可复用。同样的完整性检测可以在多个程序中使用。  

常见约束：

+ NOT NULL

+ UNIQUE

+ AUTO INCREASE

+ CHECK短语

CHECK短语：后面跟一个条件判断的布尔表达式。例如：

```sql
CHECK (Ssex = 'nv' OR Sname NOT LIKE 'MS.%')
--一句完整性约束
```

### CONSTRAINT子句

用来给完整性约束起名字，将他们以对象的方式看待。举例：  

```sql
crete table stu(
    sno int,
constraint c1 check(sno = '1')
    cno int,
constraint c2 check (cno between 1 and 3)
);
```

如果不用约束的方法，更改约束需要重新创建表，但是如果定义了约束，就可以用更改约束的方法了。  

更改方法：  

+ 更改 = 删除+增加

+ 或者直接增加

举例：  

```sql
ALTER TABLE
```


