# binascii
## Note
a2b_*()系列函数只接受Unicode编码的string（python中string的默认编码是utf-8），而且string中只能含有ascii字符。  
其他函数只能接受byte-like object，比如bytes，bytearray。  
crc32()函数返回的值要&0xffffffff。这是为了版本兼容而设计的，与运算之后才是正确的crc值。
