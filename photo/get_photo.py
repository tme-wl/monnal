import requests
from PIL import Image
import math
import os
import json


def get_photo_baidu():
    import json
    import time
    # base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E9%A3%8E%E6%99%AF&cl=&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E9%A3%8E%E6%99%AF&s=&se=&tab=&width=1024&height=768&face=0&istype=2&qc=&nc=1&fr=&pn={0}&rn=30&gsm=b4&{1}="
    base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E7%BE%8E%E5%A5%B3&cl=&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E7%BE%8E%E5%A5%B3&s=&se=&tab=&width=1366&height=768&face=0&istype=2&qc=&nc=&fr=&cg=girl&pn={0}&rn=30&gsm=1e&{1}="
    base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E7%BE%8E%E5%A5%B3&cl=&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E7%BE%8E%E5%A5%B3&s=&se=&tab=&width=1024&height=768&face=0&istype=2&qc=&nc=&fr=&cg=girl&pn={0}&rn=30&gsm=1e&{1}="
    base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E9%A3%8E%E6%99%AF&cl=&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E9%A3%8E%E6%99%AF&s=&se=&tab=&width=1024&height=768&face=0&istype=2&qc=&nc=1&fr=&pn={0}&rn=30&gsm=b4&{1}="
    base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%97%85%E6%B8%B8&cl=&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%97%85%E6%B8%B8&s=&se=&tab=&width=1024&height=768&face=0&istype=2&qc=&nc=1&fr=&pn={0}&rn=30&gsm=1e&{1}="
    base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E5%8A%A8%E6%BC%AB&cl=&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E5%8A%A8%E6%BC%AB&s=&se=&tab=&width=1024&height=768&face=0&istype=2&qc=&nc=1&fr=&pn={0}&rn=30&gsm=5a&{1}="
    base_a = 30
    base_b = 1494405802278
    name = 20000
    for i in range(100):
        url = base_url.format(base_a+(30*i),base_b+i)
        baidu_photo = requests.get(url)
        if baidu_photo.status_code == 200:
            text = json.loads(baidu_photo.text)
            if text["data"]:
                for obj in text["data"]:
                    try:
                        photo_url = obj.get("middleURL")
                        bf = requests.get(photo_url)
                        if bf.status_code == 200:
                            f = open("./"+str(name)+'.jpg','wb')
                            f.write(bf.content)
                            name += 1
                            #if name % 50 == 0:
                            print(name)
                            time.sleep(0.2)
                    except Exception as e:
                        print(e)
                        print("错误")
        else:
            print("没有"+url)
            print("错误")





def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


def get_photo_avg(photo_name):
	photo = Image.open("./bfphoto/"+photo_name)
	width =photo.width
	height = photo.height
	photo1 = photo.resize((100, int(100*photo.height/photo.width)), Image.ANTIALIAS) 
	rgblist = photo1.getdata()
	num = 0
	r=0
	g=0
	b=0
	for i in list(rgblist):
		r += i[0]
		g += i[1]
		b += i[2]
		num += 1
	avg_r = int(r/num)
	avg_g = int(g/num)
	avg_b = int(b/num)
	return (avg_r, avg_g, avg_b)

def get_photo_avg1(photo):
    width =photo.width
    height = photo.height

    photo1 = photo.resize((100, int(100*photo.height/photo.width)), Image.ANTIALIAS) 
    rgblist = photo1.getdata()
    num = 0
    r=0
    g=0
    b=0
    for i in list(rgblist):
        r += i[0]
        g += i[1]
        b += i[2]
        num += 1
    avg_r = int(r/num)
    avg_g = int(g/num)
    avg_b = int(b/num)
    return (avg_r, avg_g, avg_b)


def run(srcPath):
    """获取serPath路径下的所有图片，处理"""
    mydict={}
    i=1
    for filename in os.listdir(srcPath):
        print(i)
        i += 1
        try:
            mydict[get_photo_avg(filename)] = filename
        except:
            pass
        # mydict[srcPath] = get_photo_avg(filename)
    return mydict



def main(target_photo,x,y):
    """
    将图片target_photo 分割为横向X张，竖向Y张
    """
    photo = Image.open(target_photo)
    width =photo.width
    height = photo.height
    if int(x) == x and int(y) == y and x > 0 and y > 0 :
        one_x = width/x
        one_y = height/y
        my_photo = []
        for j in range(y):
            x_list = []
            for i in range(x):
                temp = (i * one_x, j * one_y, (i+1) * one_x, (j+1)* one_y )
                x_list.append(temp)
            my_photo.append(x_list)

        return my_photo
    else:
        return 0

# region = photo.crop(box)
  
def  haha():
    f=open("./wl.txt",'r')
    dicts = f.readlines()
    mydict = eval(dicts[0])
    wl = main("./1.jpg",20,20)
    photo = Image.open("./1.jpg")
    alls = []
    f=open("./wlphoto.txt","w")
    number = 0
    for i in wl:
        temp = []
        for j in i:
            region = photo.crop(j)
            photo_name = min_color_diff( get_photo_avg1(region) , mydict )[1]
            temp.append(photo_name)
            print(number)
            number+=1
        alls.append(temp)
    print(str(alls))
    f.write(str(alls))
    f.close()



from colorsys import rgb_to_hsv

colorsss = dict((
((196, 2, 51), "RED"),
((255, 165, 0), "ORANGE"),
((255, 205, 0), "YELLOW"),
((0, 128, 0), "GREEN"),
((0, 0, 255), "BLUE"),
((127, 0, 255), "VIOLET"),
((0, 0, 0), "BLACK"),
((255, 255, 255), "WHITE"),))

def to_hsv( color ):
    #print(color,"color")
    """ converts color tuples to floats and then to hsv """
    return rgb_to_hsv(*[x/255.0 for x in color]) 
    #rgb_to_hsv wants floats!


def color_dist( c1, c2):
    #print(c1,"c1")
    #print(c2,"c2")
    """ returns the squared euklidian distance between two color vectors in hsv space """
    return sum( (a-b)**2 for a,b in zip(to_hsv(c1),to_hsv(c2)) )

def min_color_diff( color_to_match, colors):

    """ returns the `(distance, color_name)` with the minimal distance to `colors`"""
    return min( # overal best is the best match to any color:
        (color_dist(color_to_match, test), colors[test]) # (distance to `test` color, color name)
        for test in colors)

#color_to_match = (255,255,0)
#print min_color_diff( color_to_match, colors)














def pinjie():
    # mylist是一个二维数组
    f= open("wlphoto.txt",'r')
    mylist = eval(f.readlines()[0])
    f.close()
    from PIL import Image
    temp_photo = Image.open("./bfphoto/" + mylist[0][0])
    width = temp_photo.width
    height = temp_photo.height 
    target = Image.new('RGB', ( width * (len(mylist[0])+1) , height * (len(mylist) + 1) ))  
    for x in range(len(mylist)):
        xlist = mylist[x]
        for y in range(len(xlist)):
            target_name = xlist[y]
            photo = Image.open("./bfphoto/"+target_name)

            target.paste(photo, (width * y, height* x,width * (y+1), height* (x+1) ))
    target.save("./target.jpg", quality = 100)





def pingjie():
    from PIL import Image
    photo1 = Image.open("./2.jpg")
    photo2 = Image.open("./3.jpg")
    width1 = photo1.width
    width2 = photo2.width
    height1 = photo1.height
    height2 = photo2.height
    width = width1 + width2
    height = height1 + height2
    target = Image.new('RGB', (width, max(height2,height1)))   
    target.paste(photo1, (0, 0, width1, max(height2,height1)))
    target.paste(photo2, (width1, 0, width1+width2, max(height2,height1)))
    target.save('./target.jpg', quality = 100)




import numpy as np
from PIL import Image
import glob,os
 
if __name__=='__main__':
    haha()
    pinjie()
    """
    prefix=input('Input the prefix of images:')
    files=glob.glob(prefix+'_*')
    # 所有图片
    num=len(files)
 
    filename_lens=[len(x) for x in files] #length of the files
    min_len=min(filename_lens) #minimal length of filenames
    max_len=max(filename_lens) #maximal length of filenames
    if min_len==max_len:#the last number of each filename has the same length
        files=sorted(files) #sort the files in ascending order
    else:#maybe the filenames are:x_0.png ... x_10.png ... x_100.png
        index=[0 for x in range(num)]
        for i in range(num):
            filename=files[i]
            start=filename.rfind('_')+1
            end=filename.rfind('.')
            file_no=int(filename[start:end])
            index[i]=file_no
        index=sorted(index)
        files=[prefix+'_'+str(x)+'.png' for x in index]
 
    print(files[0])
    baseimg=Image.open(files[0])
    sz=baseimg.size
    basemat=np.atleast_2d(baseimg)
    for i in range(1,num):
        file=files[i]
        im=Image.open(file)
        im=im.resize(sz,Image.ANTIALIAS)
        mat=np.atleast_2d(im)
        print(file)
        basemat=np.append(basemat,mat,axis=0)
    final_img=Image.fromarray(basemat)
    final_img.save('merged.png')
    """








