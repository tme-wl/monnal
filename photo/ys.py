#coding:utf-8

import os
from tkinter import *
from tkinter.filedialog import askdirectory

#图片压缩批处理  
# compressImage('81374758','iphone')
def fenkai_photo(srcpath):
    # 把srcpath下的图片，按照长宽比例分开
    import os
    from PIL import Image
    from fractions import Fraction as F
    allnumber = len(os.listdir(srcpath))
    num = 0
    sbfb = 0
    file_name_dict = []
    for filename in os.listdir(srcpath):
        bfb = int((num/allnumber)*100)
        num += 1
        try:
            file = Image.open(srcpath+'/'+filename)
        except:
            print("open file {0} is error".format(filename))
        else:
            w,h = file.size
            pathf = "-".join(str(F(w,h)).split("/"))
            if F(w,h) not in file_name_dict:
                file_name_dict.append(F(w,h))
                os.makedirs(srcpath+'/'+pathf)
            file.save(srcpath+'/'+pathf+'/'+filename)
            if bfb != sbfb:
                print(bfb)
                sbfb = bfb            







def compressImage(srcPath,dstPath):  
    import os
    from PIL import Image as Imagepil
    allnumber = len(os.listdir(srcPath))
    num= 0
    for filename in os.listdir(srcPath):  
        #如果不存在目的目录则创建一个，保持层级结构
        bfb = int((num/allnumber)*100)
        sbfb = 0
        num += 1
        if not os.path.exists(dstPath):
                os.makedirs(dstPath)        
        #拼接完整的文件或文件夹路径
        srcFile=os.path.join(srcPath,filename)
        dstFile=os.path.join(dstPath,filename)
        #print (srcFile, type(srcFile))
        #print (dstFile, type(dstFile))
        #如果是文件就处理
        if os.path.isfile(srcFile):     
            #打开原图片缩小后保存，可以用if srcFile.endswith(".jpg")或者split，splitext等函数等针对特定文件压缩
            try:
                sImg=Imagepil.open(srcFile)
            except:
                continue
            else:
                w,h=sImg.size  
                #print (w,h)
                if w<500:
                    dImg=sImg.resize((int(w),int(h)),Imagepil.ANTIALIAS)
                    dImg.save(dstFile)
                else:
                    temp = w/500
                    dImg=sImg.resize((int(w/temp),int(h/temp)),Imagepil.ANTIALIAS)  #设置压缩尺寸和选项，注意尺寸要用括号
                    dImg.save(dstFile) #也可以用srcFile原路径保存,或者更改后缀保存，save这个函数后面可以加压缩编码选项JPEG之类的
                #print (dstFile+" compressed succeeded")
                if bfb != sbfb:
                    print(bfb)
                    sbfb = bfb
        #如果是文件夹就递归
        if os.path.isdir(srcFile):
            compressImage(srcFile,dstFile)



def bfb(msg):
    path3.set(msg)

def selectPath1():
    path_ = askdirectory()
    path1.set(path_)


def selectPath2():
    path_ = askdirectory()
    path2.set(path_)

def qd():
    get_url = path1.get()
    put_url = path2.get()
    compressImage(get_url, put_url)

root = Tk()
path1 = StringVar()
path2 = StringVar()
path3 = StringVar()
Label(root,text = "照片文件夹:").grid(row = 0, column = 0)
Entry(root, textvariable = path1, width=40).grid(row = 0, column = 1)
Button(root, text = "路径选择", command = selectPath1).grid(row = 0, column = 3)

Label(root,text = "目标文件夹:").grid(row = 2, column = 0)
Entry(root, textvariable = path2, width=40).grid(row = 2, column = 1)
Button(root, text = "路径选择", command = selectPath2).grid(row = 2, column = 3)

Entry(root, textvariable = path3, width=40).grid(row = 3, column = 1)


Button(root, text = "确定", command = qd).grid(row = 6, column =3)



root.mainloop()


#if __name__=='__main__':  
#    compressImage("./src","./dst")
