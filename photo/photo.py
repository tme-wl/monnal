
from PIL import Image
from colorsys import rgb_to_hsv
import os


"""
Daguerre
项目说明
        处理照片为像素照片
        为达到比较好的效果，应该尽量提供更多的照片。
        照片长宽比应该一致，也就是说，若提供的都是竖向的照片，就应该所有都是竖向照片。
        最好长宽比也一致，不然部分不一致的长宽比照片会有压缩。
项目操作方法
        提供不少于5000张的，同向[1]的照片。放入tool文件夹里。
        提供一张照片为目标照明，命名为target.jpg
        按照目录
                -   tool
                -   target.jpg
                -   photo.py
        运行项目


项目具体流程
        * 图片预处理
            0   若图片少于3000张， 不执行
            1   清理所有图片格式，全为jpg, 清理到不是jpg格式的图片
            2   清理分辨率，可有指定分辨率，若没指定分辨率。以最多分辨率图片的分辨率为主
            3   压缩调整其他分辨率的图片
            4   跑图片，计算出对应的图片数据字典
        * 图片处理
            1   可指定分割,建议为40*30=1200张
            2   跑图片，生成新图片，打上标记。
"""

class Maodou(object):
    """docstring for Maodou"""
    def __init__(self, target_photo, photo_file, size_x = 20, size_y = 20):
        self.size_x = size_x
        self.size_y = size_y
        
        pass


        

def get_photo_avg(photo_name):
	"""
	将目标图片压缩为边长为100的图片 然后简单计算rgb的平均值
	"""
	photo = Image.open(photo_name)
    
	width =photo.width
	height = photo.height
	# photo1 压缩后图片
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
	# 将目标图片压缩为边长为100的图片 然后简单计算rgb的平均值
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


def all_photo_avg(srcPath):
    """获取srcPath路径下的所有图片，计算平均值写入_photoavg.txt文件"""
    mydict={}
    i=1
    for filename in os.listdir(srcPath):
        print(filename)
        print(i)
        i += 1
        try:
            mydict[get_photo_avg(srcPath + '/' +filename)] = filename
        except:
            pass
        # mydict[srcPath] = get_photo_avg(filename)
    f = open(srcPath + '_photoavg.txt', 'w')
    f.write(str(mydict))
    f.close()
    return True


def split_photo_func(target_photo,x,y):
    """
    将图片target_photo 分割为横向X张，竖向Y张
    """
    print("in split")
    photo = Image.open(target_photo)
    print("open")
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


def calculate(photodata, target_photo, split_photo, x=20, y=20):
	# 计算图片
    f=open(photodata, 'r')
    dicts = f.readlines()
    mydict = eval(dicts[0])
    print("in")
    print(target_photo)
    wl = split_photo_func(target_photo=target_photo, x=x, y=y)
    #wl = split_photo_func()
    photo = Image.open(target_photo)
    alls = []
    f=open(split_photo,"w")
    number = 0
    for i in wl:
        temp = []
        for j in i:
            region = photo.crop(j)
            photo_name = min_color_diff( get_photo_avg1(region) , mydict )[1]
            for key in mydict:
            	if mydict[key] == photo_name:
            		delete_name = key
            		break
            mydict.pop(delete_name)
            temp.append(photo_name)
            print(number)
            number+=1
        alls.append(temp)
    print(str(alls))
    f.write(str(alls))
    f.close()


def tag_and_save(photo,size,file_name):
    # size是一个坐标 [2,1]
    # photo 是一个image类
    # file_name为新照片存储地方
    from PIL import ImageDraw,ImageFont
    font = ImageFont.truetype('Arial.ttf',24)
    draw = ImageDraw.Draw(photo)
    draw.text((photo.width-60, photo.height-30), str(size), (255, 0, 0), font=font)
    draw = ImageDraw.Draw(photo)
    photo.save('new'+photo.filename)


def pinjie(file_name,source):
    # mylist是一个二维数组
    f= open(source,'r')
    mylist = eval(f.readlines()[0])
    f.close()
    temp_photo = Image.open(file_name+"/" + mylist[0][0])
    photo1 = temp_photo.resize((100, int(100*temp_photo.height/temp_photo.width)), Image.ANTIALIAS) 
    width = photo1.width
    height = photo1.height  
    print(width,height,"图片宽度高度")
    new_photo_width = width * (len(mylist[0])+1)
    new_photo_height = height * (len(mylist) + 1) 
    print(new_photo_width,new_photo_height,"新图片宽度高度")
    target = Image.new('RGB', (new_photo_width, new_photo_height))  
    for x in range(len(mylist)):
        xlist = mylist[x]
        for y in range(len(xlist)):
            target_name = xlist[y]
            print(file_name + "/" +target_name)
            print("open photo name")
            photo = Image.open(file_name + "/" +target_name)
            photo1 = photo.resize((100, int(100*photo.height/photo.width)), Image.ANTIALIAS) 
            print((photo1.width * y, photo1.height* x, photo1.width * (y+1), photo1.height* (x+1) ))
            target.paste(photo1, (photo1.width * y, photo1.height* x, photo1.width * (y+1), photo1.height* (x+1) ))
    target.save(file_name + "_target.jpg", quality = 100)



def to_hsv( color ):
    """ converts color tuples to floats and then to hsv """
    return rgb_to_hsv(*[x/255.0 for x in color]) 
    #rgb_to_hsv wants floats!

def color_dist( c1, c2):
    """ returns the squared euklidian distance between two color vectors in hsv space """
    return sum( (a-b)**2 for a,b in zip(to_hsv(c1),to_hsv(c2)) )

def min_color_diff( color_to_match, colors):
    """ returns the `(distance, color_name)` with the minimal distance to `colors`"""
    return min( # overal best is the best match to any color:
        (color_dist(color_to_match, test), colors[test]) # (distance to `test` color, color name)
        for test in colors)


if __name__ == "__main__":
	# all_photo_avg("4-3")

	calculate("4-3_photoavg.txt", "bfphoto.jpg", "bfphoto_split.txt", x=20, y=20)

	pinjie("4-3","bfphoto_split.txt")



