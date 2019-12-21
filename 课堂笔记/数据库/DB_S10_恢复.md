# 数据库恢复

这一节主要是针对一致性和事务的概念进行分析。

## Transaction

### Defination

a sequencial operations of Database.  

a unseparateable work unit（要么都做，要么都不做）

atom unit of Recovery and Cocurrency

### Definate by SQL

显式定义方式

```sql
BEGIN TRANSACTION
SQL 语句1
SQL 语句2
...
COMMIT
```

### Characteristic（ACID）

+ Atomicity 原子性：要么全部执行，要么全不执行

+ Consistency 一致性：执行事务之前数据库是一致的，那么执行之后也一定要一致

+ Isolation 隔离性：即使并发执行，每个事务也感觉不到其他事务的存在，这保证了一致性

+ Durabiliry 持续性：成功执行之后对数据库的修改是永久的，即使系统出故障

## 故障

不可避免：系统or人为故障  

恢复的概念：从错误状态恢复到某一已知的正确状态（也称为一致状态，完整状态）  

恢复子系统是DBMS非常重要的组成部分！

更多的故障时非预期的：

+ 运算溢出

+ 并发事务死锁

+ 违反了某些完整性限制

恢复的方法是UNDO（撤销事务）

### 系统故障

恢复方法：

+ 如果未提交，强行UNDO所有未完成事务。

+ 如果已提交，但缓冲区信息还没写入磁盘，进行REDO。

## 恢复的实现

### 转储

就是备份

### 日志

原则

+ 严格按照事务中次序执行

+ 必须先写日志在写数据库

+ 日志文件的操作也要记录

+ 数据库的修改要记录

### Checkpoint TECH

是为了避免大量的REDO。就是存档  

动态维护日志文件

策略：

+ 检查点开始的事务全都放到UNDO队列

+ 从检查点扫到故障点（日志结束点），扫到commit的了，就放到REDO队列

### Mirror TECH

每次更新，都复制到MIRROR，始终保持与主数据库的同步

正常运行的时候，镜像源也可以提供read服务。
