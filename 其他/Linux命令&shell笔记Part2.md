# 命令:cat/script/find/tr

## cat：读取/显示/拼接

cat可以读取很多个文件。`cat f1 f2 f3`  

+ -s:把多个空行压缩成单个输出
+ -t:可以把制表符\t单独显示成为`^I`
+ -n:加入行号

## script：录制命令

```bash
script -t 2> timing.log -a output.session
type commands;
...
...
exit
# 将时序序列输出到timing.log，命令输出到output.session
```

## find：文件查找和列表

### 基本搜索

`find base_path`，这个路径可以是任何位置，find会递归地寻找路径下所有文件，匹配符合条件的文件，并执行相应操作。  

+ -name：根据文件名搜索，支持通配符：`find . "file*" -print`。如果使用-iname ，则可以忽略大小写。
+ -o：用来当做OR条件。在使用条件是，可以利用 \\(...\\) 这种方式把条件视为一个整体。`find . \( -name "*.txt" -o -name "*.pdf" \) -print`**一定注意空格不能省略**
+ -path：可以匹配文件路径或文件，支持通配符。
+ -regex：基于正则表达式匹配， -iregex可以忽略大小写。
+ ！可以否定参数的含义。`find . ! -name "*.txt" -print`意思匹配非txt后缀的文件。
+ -mindepth,-maxdepth：限制搜索的深度。这个参数不应该太靠后，否则会影响效率。

### 根据类型参数搜索

-type参数可以对文件类型进行过滤。比如：`find . -type d -print`代表只列出所有的目录。

+ f：普通文件
+ l：符号链接
+ d：目录
+ c：字符设备
+ b：块设备
+ s：套接字
+ p：Fifo

### 其他搜索选项

根据文件时间：-atime,-mtime,-ctime分别代表访问时间，修改时间，变化时间。变化时间是指文件的metadata(比如权限或所有权)改变的时间。这个是以天为单位的，而与符号+-结合可以表示大于小于这个天数的意思。  
-amin,-mmin,-cmin可以以分钟为单位  

```bash
$ find . -type f -atime -7 -print
$ find . -type l -amin +10 -print
```

根据文件大小：-size选项。单位可以有b/c/w/k/M/G，注意b代表块，是512字节的含义；c代表字节；w代表字，即2字节。

```bash
$ find . -type f -size +2k -print
$ find ../ -type f -size 2M -print
```

根据所有权：-perm参数，之后接权限的数字即可。

```bash
$ find . -type f -perm 644 -print
```

删除匹配的文件：-delete选项即可。  

跳过指定的目录:-prune选项。用法比较玄学，需要写在一个语句块中。

```bash
$ find gittest/test1 \( -name ".git" -prune \) -o \( -type f -print)
```

### 结合其他命令操作

-exec选项可以后接命令。在这个命令中，{}是一个特殊的字符串，它会被替换成匹配到的文件名。

```bash
$ find . -type f -name "*.c" -exec cat {} \;>all_c_files.txt
#当前目录所有c程序整合到单个文件。
#为什么不用>>？因为find的全部输出只是一个单数据流，stdin。如果有多个数据流被追加到文件就有必要使用了。
$ find . -type f -mtime +10 -name "*.txt" -exec cp {} OLD \;
#把十天前的txt文件复制到OLD目录中
```

## tr：字符替换、压缩、转换

tr只能通过stdin，不能通过命令行参数接受输入。调用格式如下：`tr [options] set1 set2`，其中set表示集合，可以通过输入元素定义集合，也可以用起始字符-终止字符的方式定义集合。  
如果set2的长度比set1小，那么set2将会重复它的最后一个元素。如果比set1大，则会截断多余的部分。

```bash
$ echo hello | tr 'a-z' 'A-Z'
HELLO
$ echo 123456789 | tr '1-9' '132457689'
132457689
$ echo hello,world! | tr 'a-z' 'd-zabc'
khoor,zruog!
#凯撒密码
```

### -c，-d，-s 选项

可以通过-d选项进行字符删除，此时只需要输入set1就可以。  
-c选项定义了一个集合的补集，经常和-d一起使用。

```bash
$ echo "hello 123 world 456" | tr -d '0-9'
hello  world
$ echo "emmm 1I 2want 3numbers 4" | tr -d -c '0-9 \n'
#除了0-9和空格换行，全部删除
 1 2 3 4
```

-s选项可以压缩重复的字符，变成单个字符。用法是`tr -s set1`  
常用来压缩空白字符。

### 字符类

可以像使用集合一样使用这些字符类，语法是`tr '[:class1:]' '[:class2:]'`  

+ alnum 字母和数字
+ alpha 字母
+ cntrl 控制字符
+ digit 数字
+ lower 小写字母
+ punct 标点符号
+ space 空白字符
+ upper 大写字母
+ xdigit 十六进制字符
+ print 可打印字符

```bash
$ echo "$0sch^as98dh*"|tr -d '[:alnum:]'
-^*
```