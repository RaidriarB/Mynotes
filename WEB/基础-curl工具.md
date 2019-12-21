# curl

curl是一种命令行工具，作用是发出网络请求，然后得到和提取数据，显示在"标准输出"（stdout）上面。  
它支持多种协议。  

## 命令

[中等详细命令博客](http://www.ruanyifeng.com/blog/2019/09/curl-reference.html)

基础：获得源码/headers/通信过程

```bash
#直接看源码
curl www.sina.com
#保存到文件
curl -o [文件名] www.sina.com
#自动跳转（比如这个跳转到了www.sina.com.cn)
curl -L www.sina.com
# 显示http Headers信息连同网页源代码
curl -i www.sina.com
# 只显示Headers不显示网页源代码
curl -I www.sina.com

# 显示整个通信过程
curl -v www.sina.com
#更详细的通信过程
curl --trace [输出到文件名称] www.sina.com
curl --trace-ascii [输出到文件名称] www.sina.com
```

HTTP动词

```bash
#默认是GET
curl example.com/form.cgi?data=xxx
#如果想替换成其他的动词，要用-X指定。POST：数据要和url分离
curl -X POST --data "data=xxx" example.com/form.cgi
curl -X POST www.example.com
curl -X DELETE www.example.com
#如果你的数据没有经过表单编码，还可以让curl为你编码
curl -X POST--data-urlencode "date=April 1" example.com/form.cgi

#文件上传：假设表单是这样
#
# <form method="POST" enctype='multipart/form-data' action="upload.cgi">
#   <input type=file name=upload>
#   <input type=submit name=press value="OK">
# </form>
curl --form upload=@localfilename --form press=OK [URL]
```

HTTP headers

```bash
# Referer：你从哪里跳转过来
curl --referer http://www.example.com http://www.example.com
#User-agent：用户客户端信息
curl --user-agent "[User Agent]" [URL]
curl -A "[User Agent]" [URL]

#cookie
curl --cookie "name=xxx" www.example.com
#发送cookie
curl -b "name=x" -b "age=y" www.example.com
#保存cookies到文件
curl -c [file] http://www.example.com
# 使用文件中的cookie进行请求
curl -d [file] http://www.example.com

#认证
curl --user name:password example.com
#增加一些header
curl --header "Content-Type:application/json" http://example.com
curl -H "Content-Type:application/json" http://example.com
```