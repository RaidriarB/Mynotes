# Docker 实际应用

## SQLServer

### 初次使用

下载  

```docker
sudo docker pull microsoft/mssql-server-linux:2017-latest
映射+运行
```

映射端口+运行。MSSQL端口默认为1433  

```docker
sudo docker run -e &#39;ACCEPT_EULA=Y&#39; -e &#39;MSSQL_SA_PASSWORD=bjm123456!&#39; -p 1401:1433 --name MSSQL_Test -d microsoft/mssql-server-linux:2017-latest
```

在docker server 端登录并且设置SA密码  

```docker
sudo docker exec -it MSSQL_Test /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P &#39;bjm123456!&#39; -Q &#39;ALTER LOGIN SA WITH PASSWORD="bjm123456!"&#39;
```

执行bash  

```docker
sudo docker exec -it MSSQL_Test "bash"
```

启动服务端程序  

```docker
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'bjm123456!'
```

Ctrl+P——Ctrl+Q组合退出，变为守护进程，客户端连接即可。  

### 再次使用

```docker
docker start -i MSSQL_Test
```

## mysql

### 初次使用

创建mysql容器并映射端口，mysql的默认端口是3306  

```docker
docker run -id --name=mysql_test -p 33306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
```

进入容器，执行bash  

```docker
docker exec -it mysql_test /bin/bash
```

用刚设定的密码123456登录  

```sql
Mysql -u root -p
123456
```

进入了mysql>的界面。  

可以输入status查看版本信息，一般是8.0以上  

### 授权远程连接的方法

授权：所有权限都给root  

```sql
GRANT ALL ON *.* TO &#39;root&#39;@&#39;%&#39;;
```

刷新权限  

```sql
flush privileges;
```

更改加密规则，8.0以后的加密规则有所改变。EXPIRE含义是过期时间  

```sql
ALTER USER &#39;root&#39;@&#39;localhost&#39; IDENTIFIED BY &#39;password&#39; PASSWORD EXPIRE NEVER;
```

更改root用户密码  

```sql
ALTER USER &#39;root&#39;@&#39;%&#39; IDENTIFIED WITH mysql_native_password BY &#39;123456&#39;;
```

刷新权限  

```sql
flush privileges;
```

现在可以远程连接mysql数据库了  

### 再次使用

```docker
docker start -i mysql_test
```

## lamp

顺便把容器80端口映射到本机8088，再把容器中/var/www/example.com/public_html绑定到本机当前文件夹下的public_html

```bash
docker run --name lampTest -p 8088:80 --volume `pwd`/public_html:/var/www/example.com/public_html/ -i -t linode/lamp /bin/bash
```

然后在当前目录新建public_html，就可以了。

## Nikto

```bash
docker run --rm -t kenney/nikto:latest nikto -h http://nctf2019.x1ct34m.com:60003/
```
