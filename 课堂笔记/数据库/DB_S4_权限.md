# Safety

## 1.DAC

自主访问控制机制中数据的拥有者可以任意修改或授予此数据相应的权限。  
权限组成：数据对象，操作类型  
数据对象：  

+ schema
+ table
+ view
+ index
+ column

## GRANT & REVOKE

可以发出GRANT的用户：DBA or 数据库对象创建者（Owner） or 拥有该权限的用户。  
接收权限的用户； public or 具体一个用户  
WITH GRANT OPTION：给出权限后，可以再授予或者不能传播。  

可以使用REVOKE收回，CASCADE进行递归收回。

### e.g.  GRANT

以下的u1，u2等代表一个用户。  

```sql
grant select  
on table student  
to u1;
```

```sql
grant ALL PRIVILIGES  
on table student
to u2,u3;
```

```sql
grant select  
on table sc  
to public;
```

```sql
grant update(sno) , select  
on table studnet   
to u4;
```

```sql
grant insert  
on table sc  
to u5  
with grant option;
-- 可以将这个权限授予别人。
```

### e.g. REVOKE

```sql
revoke update(sno)
on table student
from u4;
```

```sql
revoke select
on table sc
from public;
```

```sql
revoke insert
on table sc
from u5 CASCADE;
--cascade:级联回收，收回直接或间接从u5获得的权限。递归执行。
```

### 基本知识：DB ROLE

类似Windows中的User group，是RBAC（基于角色的访问控制）  
可以创建角色。语法如下；
`create role <角色名>`  
然后给角色授权/收回，就像给普通用户授权那样。此时也可以将一个角色的权限给另一个角色。  
重点：用户加入到角色  
`GRANT <rolename> TO user1,user2,...`  
角色的权限可以随时修改

### 关于创建的权限

创建数据库模式的权限？这是在创建用户的时候指定的。  
`create user <username> [with] [DBA | RESOURCE | CONNECT]`  

+ DBA：可创建用户，基本表，模式，可CRUD(并且不需要特殊赋予权限)
+ RESOURCE：不可创建用户和模式，可创建基本表，可CRUD(并且不需要特殊赋予权限)
+ 不可以创建，只能在给定权限下CRUD

## 2.MAC

强制访问控制机制中不允许数据的拥有者随意修改或授予此对象相应的权限，而是通过强制的方式为每个对象分别授予权限。  
根据客体的密级和主体的许可证级别进行访问控制。  

### 规则

+ 主体级别 大于等于 客体密级  -> 可以读  
+ 主体级别 等于 客体密级  -> 可以写

也有修正规则：主体级别 小于等于 客体密级 -> 可以写

规则思想：安全性不能高->低，防止越权访问，跨越安全边界。  
根据这个思想，可以构造一些其他访问控制的逻辑漏洞。  

## 3.SQL server的安全机制

注意：用户和登录名并不是一回事，登录名是登入sqlserver时用的，而用户是针对数据库的权限而言。一个用户可以对应多个登录名。  

存储过程：sqlserver的一些小程序，是一些命令，和一般的SQL语句不一样。

### 登录认证

+ Windows认证方式（直接登录到windows中就可以）

+ 混合认证模式

### 用户的管理

1. dbo用户：数据库的拥有者，具有其拥有的数据库所有的操作权限。

2. guest用户

### 角色的管理

即RBAC的管理思想