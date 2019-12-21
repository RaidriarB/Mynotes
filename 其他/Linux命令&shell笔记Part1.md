# 基本知识

## shell提示符和shell脚本文件

+ `username@hostname$`代表普通用户，`root@hostname#`代表超级用户  
+ shell脚本文件是以`!#[解释器路径]`开头的文件。比如`#!/bin/bash`  
+ 想要运行shell脚本，可以用解释器执行：`sh script.sh`，或者直接执行脚本：`./script.sh`（注意前面的./不能省略）或使用脚本完整路径：`/.../script.sh`。直接执行脚本需要有可执行的权限，如果没有的话会`zsh: permission denied: ./script.sh`。此时需要`chmod a+x script.sh`。

## 终端打印：echo、printf

关于echo

+ 每次打印加一个换行符。
+ 不带引号，单引号和双引号都可以打印，但有细微的差别：双引号中不能打印感叹号'!'，需要转义。不带引号不能打印分号（因为被用作定界符），单引号中的变量$var不会被求值。
+ 一些选项：-n：忽略结尾的换行符；-e：包含转义序列
+ 打印彩色的例子`echo -e "\e[1;31m This is red Text. \e[0m"`，其中最后的`\e[0m`把颜色重新置回，第一个`\e[1;31m`把颜色设置成了红色

关于printf

+ 和C语言中的printf很相似，注意每次使用都会在结尾附加一个\n
+ 格式：printf "[%[-a][.b][格式替代符：s/c/d/f...]]..." var1 var2...

```bash
$ printf "%-3s,%-10s,%-4.2f" 1 Raidriar 2.333333
1  ,Raidriar  ,2.33
```

## 变量与环境变量的使用

变量

+ 这样是给变量赋值：`var=value`，这样是判断相等：`var = value`
+ 在变量前面加上`$`前缀，即可对变量求值。例如`echo $var`
+ 获得变量长度：`${#var}`

环境变量是未在当前进程中定义，而是从父进程继承的变量。例如`PATH`

+ export命令可以设置环境变量:`export PATH="$PATH:/..."`
+ 还有一些环境变量`HOME PWD USER UID SHELL`

```bash
#!/bin/bash
echo $PATH;echo $HOME;echo $PWD;echo $USER;echo $UID;echo $SHELL
# script.sh
```

```bash
raidriarb@Rmbp LinuxShellTest % ./script.sh 
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Apple/usr/bin:/Library/Apple/bin:/Applications/Wireshark.app/Contents/MacOS
/Users/raidriarb
/Users/raidriarb/Desktop/LinuxShellTest #PWD：当前工作目录
raidriarb
501 #UID为0，则为root用户
/bin/zsh #现在用的shell是哪个
```

## 数学

## 文件描述符与重定向

### 基础知识

文件描述符是与【一个打开的文件或数据流】相关联的【整数】。IO编程中，我们经常使用到`stdin,stdout,stderr`这几个流，这几个流的文件描述符是系统预留的，分别为`0,1,2`  

+ 关于stderr：很多人不知道它是做什么用的，这个流用来打印错误信息。它虽然在控制台中打印了文本，但并非标准输出stdout的方式打印，否则是区分不开错误信息的文本和正常文本的。
+ 命令执行成功和不成功是有返回值的，这个返回值通过变量`$?`来查看

```bash
$ ls +
ls: +: No such file or directory #这是stderr打印的

$ echo $?
1 #不成功
$ echo $?
0 #上一条的echo $? 是成功的
```

文件重定向的符号有两个：`>`和`>>`。其中前者的输出方式是“清空”，后者的输出方式是“追加”。

```bash
$ echo "hello1" > hello
$ cat hello
hello1

$ echo "hello2" > hello
$ cat hello
hello2

$ echo -n "hello3" >> hello
$ cat hello
hello2
hello3
```

当然也可以重定向stderr，这里不多演示了。  
如果重定向到了这个文件：`/dev/null`，那么所有的输出都会被丢弃。这个文件也被称为黑洞。

### 管道和tee命令

管道的符号是`|`，它可以把上一个命令的输出，作为stdin，传给下一个命令。注意只有在管道的最后才会被输出。

```bash
$ cat file1 | cat -n
     1	this is a line in file1.
     2	this is another line.
```

如果使用了重定向，那么输出从stdout重定向了，没有什么东西可以通过管道传递给接下来的命令。  
命令tee可以提供一种方法，将一份副本写入重定向的文件，同时把另一份副本传递给后续命令的stdin。

```bash
$ cat file1 | tee file1_cp | cat -n
     1	this is a line in file1.
     2	this is another line.
#既输出到了文件，又通过管道传输给下一个命令
```

+ tee默认情况是覆盖方式写入文件，但 -a 参数可以使用追加模式
+ stdin也可以作为tee的参数，只要把`-`或者`/dev/stdin`作为文件名参数即可
+ 同样的，`/dev/stdout,/dev/stderr`代表标准输出和标准错误流

## 其他技巧

### 别名 alias

+ 别名是一种快捷方式，可以替换一长串命令。  
+ 例如`alias rm 'cp $@ ~/backup; rm $@'`，可以防止rm -rf从删库到跑路  
+ 一旦关闭当前终端，别名就会失效。如果要持久化，需要将它写入~/.bashrc文件中:`echo 'alias cmd="command seq"' >> ~/.bashrc`
+ 使用转义命令`\command`可以强制使用原命令command，而不是别名，所以强制删库跑路也是可以的。。。为了安全起见，建议在不信任的环境下的命令都加上这个转义序列，因为可能有人在此目录植入了别名，更换了一些别有用心的命令