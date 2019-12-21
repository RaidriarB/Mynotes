# Note and exercise on SQL Class

## index
create cluster index stuname on student (sname) -- 聚簇索引  
-- 经常更新的表不适合聚簇索引  
create unique index stusno ON student(sno)  
create unique index concno on course(con)  
create unique index scno on sc(sno asc,cno dec);  
-- pk index usually be automatically created  

## INSERT

grammar: insert into <tablename> [<column>[,<column2>...]] values (...)  
insert into (sno , sname , sex) values ('asd','asd','asd)  
--always used as register logic  

可以不指定属性名，那就要所有的信息。这不是一个好的写法。属性名可以防止误操作，也方便null值处理  

insert into sc(sno,cno) values ('asd','1')  
--RDBMS automatically give a NULL value to where not indicated  

插入的value可以是子查询。  
比如：  
example:  
create table da(snosdept char(15)  
avg_age smallint);  
insert into da(sd,aa)  
select Sdept ,avg(age)  
from student group by sdept  

## UPDATE

syntax: update <tablename> set <columnname>=<expression>[<>=<>...] [where <condition>]  
e.g.  
updat student set sage=22 where sno='2018213639'  
如果不加where，默认对所有的元祖都更改！  
update student set sage = sage+1  
--这就是所有的学生年龄都加1  

## DELETE

e.g.  
delete from student where sno='asdasd'  
delete from sc  
--这样就全部删除了，但表的模式本身还在，只是没有元租了。
drop table:整个表都没有了
在删除时，要注意完整性约束！如果不满足了，操作会失败。
三个完整性：pk约束，fk约束，用户定义的约束。

## VIEW

作用：自行体会。  
独立性，安全保护  

### Create

syntax:  
注意，子查询不能含有orderby和distinct短语。

```sql
create view <name> [<column>...]  
AS <子查询>  
[with check option]  
```

并非真正子查询，而是存储语句，当查找视图的时候会根据定义去查询数据。（虚表）  
e.g.  

```sql
create view IS-STU  
AS  
SELECT sno,sname,sage  
FROM Student  
WHERE Sdept = 'IS'  
```

with check option 的选项:保证修改删除插入等等时候，自动加上where中的条件，保证完整性。如果插入的时候where制定的属性没有定义值，则会自动定义这个值，让它符合where的条件。

语法上，可以不指定属性列.  

```
create virw f (...)
as
select *
from student
where ssex='F'
```
这依赖于表的结构不变，但是如果以后的维护有变，这个视图指定的属性列就会不匹配。所以很不推荐这样做。  

### 查询视图

DBMS使用视图消解法进行查询。  

+ 进行有效性检查
+ 转化为基本表的查询
+ 执行基本表查询

例如已有视图：

```
create view iss  
as  
select snomsname,sage  
from student  
where sdept='IS'
```
直接用视图的查询语句：

```
select sno,sage  
from iss  
where sage <20
```

### UPDATE

+ 注意：有些视图不可更新，因为不能唯一转换成对基本表的更新。  
比如聚集函数产生的视图（多个值变为一个值）  

+ 行列子集视图可以更新。
+ DBMS规定了一些可以更新和不可更新的情况。




