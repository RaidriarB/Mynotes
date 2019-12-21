# Linux:网络命令

## ifconfig/route/nslookup/host

### ifconfig

用来显示网络接口，子网掩码等详细信息。location:`/sbin/ifconfig`。  

每个系统默认存在一个接口`lo`，是环回接口，指向主机本身。

```bash
raidriarb@Rmbp ~ % ifconfig
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
    options=1203<RXCSUM,TXCSUM,TXSTATUS,SW_TIMESTAMP>
    inet 127.0.0.1 netmask 0xff000000 
    inet6 ::1 prefixlen 128 
    inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1 
    nd6 options=201<PERFORMNUD,DAD>
```

+ 输入`ifconfig iface_name`可以只显示`iface_name`网卡的信息。

+ 可以设置网络接口的IP和子网掩码。`ifconfig iface_name <IP> netmask <mask>`，可只设置IP或只设置掩码也可以一起设置
