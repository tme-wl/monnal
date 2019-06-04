import os
import json
from colorsys import rgb_to_hsv
from PIL import Image

from common import GetFileMd5, GetStrMd5, Base
from clear import ClearPhoto
from calculate import Calculate
from common import PHOTO_SUFFIX


photo_db = {
    "photos_md5": "adfadfadadsf",
}

def get_photo_avg(photo):
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


class Monet(Base):
    """主莫奈函数"""

    def check(self):
        # 检查源photos图库有无更新 检查md5值 若有更新 重新计算图片数据值
        p_list = os.listdir(self.photos_path)
        #列出文件夹下所有的目录与文件
        print(p_list)
        md5s = []
        clear_photos = {}
        all_count = len(p_list)
        print("检查md5")
        Speed = []
        for i in range(all_count):
            # 获取每个文件的md5,排序,相加再求md5
            # 检查后缀
            speed = int(float(i)/all_count * 100)
            if speed not in Speed:
                print(str(speed) + "%")
                Speed.append(speed)
            suffix = p_list[i].split('.')[-1]
            if suffix not in PHOTO_SUFFIX:
                continue
            path = os.path.join(self.photos_path,p_list[i])
            if os.path.isfile(path):
                _md5 = GetFileMd5(path)
                if _md5 not in md5s:
                    md5s.append(_md5)
        md5s.sort()
        photos_md5s = GetStrMd5("".join(md5s))
        photos_md5 = self.db.get("photos_md5")
        print(photos_md5)
        print('photos_md5')
        print(photos_md5s)
        print('photos_md5s')
        print("检查MD5完成")
        return photos_md5s == photos_md5

    def splits(self, x):
        # 传入一个图片类 把图片分割为若干小图片 只计算坐标
        # x为横向张数 纵向按比例算
        photo = Image.open(self.target_path)
        width =photo.width
        hight = photo.height
        print(width, hight)
        y = int(x * hight / width)
        print(x, y)
        one_x = width/x
        one_y = hight/y
        my_photo = []
        for j in range(y):
            x_list = []
            for i in range(x):
                size = (i * one_x, j * one_y, (i+1) * one_x, (j+1)* one_y )
                x_list.append(size)
            my_photo.append(x_list)
        return my_photo
    
    def similar(self, color_to_match, colors):
        """寻找相似的图片
        遍历图库 寻找最小hsv差
        """
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
                # (distance to `test` color, color name)
                (color_dist(color_to_match, colors[test]), colors[test])
                for test in colors)
        return min_color_diff( color_to_match, colors)

    
    def split_join(self, photos):
        # 拼接为一张大图
        # f= open(source,'r')
        # mylist = eval(f.readlines()[0])
        # f.close()
        # temp_photo = Image.open(file_name+"/" + mylist[0][0])
        # photo1 = temp_photo.resize((100, int(100*temp_photo.height/temp_photo.width)), Image.ANTIALIAS) 
        # width = photo1.width
        # height = photo1.height  

        mini_photos = os.path.join(self.photos_path, ".miniphoto")
        lists = os.listdir(mini_photos) 
        if not lists:
            return None
        one_mini_photo = os.path.join(mini_photos, lists[0])
        one_mini_photo_obj = Image.open(one_mini_photo)
        width = one_mini_photo_obj.width
        height = one_mini_photo_obj.height  


        new_photo_width = width * (len(photos[0])+1)
        new_photo_height = height * (len(photos) + 1) 
        print(new_photo_width,new_photo_height,"新图片宽度高度")
        target = Image.new('RGB', (new_photo_width, new_photo_height))  
        for x in range(len(photos)):
            xlist = photos[x]
            for y in range(len(xlist)):
                target_name = xlist[y]

                # print(file_name + "/" +target_name)
                # print("open photo name")
                # photo = Image.open(file_name + "/" +target_name)
                # photo1 = photo.resize((100, int(100*photo.height/photo.width)), Image.ANTIALIAS) 

                photo1 = Image.open(os.path.join(mini_photos, target_name))
                # print((photo1.width * y, photo1.height* x, photo1.width * (y+1), photo1.height* (x+1) ))
                target.paste(photo1, (photo1.width * y, photo1.height* x, photo1.width * (y+1), photo1.height* (x+1) ))
        print(self.target_save_path, 'save_path')
        target.save(self.target_save_path + "/_target.jpg", quality = 100)

    def run(self):
        check_md5 = True
        # check_md5 = self.check()
        if not check_md5:
            # 数据源有改动 另算
            print("数据源有改动")
            clear = ClearPhoto()
            clear.run()
            color = Calculate()
            color.run()

        photo_db = self.get_db().get("photo_db")
        photos = self.splits(self.width)
        target_photo = Image.open(self.target_path)
        alls = []
        for p_x in photos:
            temp = []
            for p_y in p_x:
                region = target_photo.crop(p_y)
                limit_photo_value = self.similar( get_photo_avg(region) , photo_db )[1]
                print(limit_photo_value, '')
                limit_photo_name = list(photo_db.keys())[list(photo_db.values()).index(limit_photo_value)]
                print(limit_photo_name, 'limit_photo_name')
                temp.append(limit_photo_name)
            alls.append(temp)
        self.split_join(alls)

    def test(self):
        self.run()

if __name__ == '__main__':
    a = Monet()
    a.test()
      
