# Introduction
PIL是python一个图像处理库，主要功能有：缩略图，转换图像格式，打印图像，图像展示，图像处理。  
PIL包括了基础的图像处理函数，包括对点的处理，使用众多的卷积核(convolution kernels)做过滤(filter),还有颜色空间的转换。PIL库同样支持图像的大小转换，图像旋转，以及任意的仿射变换。PIL还有一些直方图的方法，允许你展示图像的一些统计特性。这个可以用来实现图像的自动对比度增强，还有全局的统计分析等。
# 用法

首先是Image类：核心类  
from PIL import Image
## 创建图像对象
Image.new(mode,size)  
`im = Image.new("RGBA",(100,200))`
 Image.open(filename,mode)  
`im.open("test.png","r")`  
一些属性:size,mode,format  
`print(im.size,im.mode,im.format)`  
展示图片`im.show()`
## 保存图片
Image.save(filename,format)  
`im.save("test2.png",'png')`
## 创建缩略图 
None Image.thumbnail(size,resample)  
注意！这个是原地操作  
`im.thumbnail((50,50),resample=Image.BICUBIC)`
## 裁剪区域 
crop(box)
```
box = (10,10,100,100)
region = im.crop(box)
region.show()
```
## 图片旋转或翻转 Image.transpose(method)
`nim = im.transpose(Image.ROTATE_180)`  
    - Image.FLIP_LEFT_RIGHT,左右翻转  
    - Image.FLIP_TOP_BOTTOM,上下翻转  
    - Image.ROTATE_90,逆时针旋转90°  
    - Image.ROTATE_180,逆时针旋转180°  
    - Image.ROTATE_270,逆时针旋转270°  
    - Image.TRANSPOSE,转置(相当于顺时针旋转90°)  
    - Image.TRANSVERSE,转置,再水平翻转  
## 粘贴 
paste(region,box,mask)  
`im.paste(region,(20,20),None)`
## 颜色通道分离 
Image.split()
```
r,g,b = im.split()
r.show()
g.show()
b.show()
```
## 颜色通道合并 
static Image.merge(mode,channels)  
`nim = Image.merge("RGB",[b,r,g])`
## 获取像素点
```
im = Image.open('image.gif')
rgb_im = im.convert('RGB')
r, g, b = rgb_im.getpixel((1, 1))

print(r, g, b)
(65, 100, 137)
```
## 转换大小 
Image.resize(size,resample,box)
```
nim = im.resize((50,50))
mim = im.resize(50,50,box=(10,10,90,90))
```
## 改变模式
Image.convert(mode,matrix,dither,palette,colors)  
mode,一般是'RGB'(真彩图)、'L'(灰度图)、'CMYK'(压缩图)  
## 过滤器
Image.filter(filter)
`from PIL import ImageFilter`  
在PIL.ImageFilter函数中定义了大量内置的filter函数，比如BLUR(模糊操作),GaussianBlur(高斯模糊),MedianFilter(中值过滤器)，FIND_EDGES(查找边)等。
```
nim = im.filter(ImageFilter.BLUR)
mim = im.filter(ImageFilter.FIND_EDGES)
```
## 对图像的像素操作 
Image.point(lut,mod)  
第一个参数传入一个函数或lambda表达式。  
比如：把所有像素放大1.5倍
```
nim = im.point(lambda x:x*1.5)
nim.save("nim.png","png")
```
## 获取gif序列
```
gif = Image.open("samp.gif")

for i,frame in enumerate(ImageSequence.Iterator(gif),1):
    if frame.mode == "JPEG":
        frame.save("%d.jpg"%i)
    else:
        frame.save("%d.png"%i)

```
