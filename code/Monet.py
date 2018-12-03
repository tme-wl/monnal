import ConfigParser 
import os
import json

from PIL import Image

from common import GetFileMd5, GetStrMd5


photo_db = {
    "md5": "adfadfadadsf",

}



class Monet(object):
    """主莫奈函数"""

    def __init__(self):
        # 读取配置
        config=ConfigParser.ConfigParser()
        config.read(os.getcwd() + '/config.ini')
        # 目标图片路径
        self.target_path = config.get('path', 'TARGET_PHOTO')
        # 图片库路径
        self.photos_path = config.get('path', 'PHOTOS')
        # 设置宽高
        self.width = config.get('size', 'WIDTH')
        self.hight = config.get('size', 'HIGHT')
        # 是否重复
        self.repeat = config.get('other', 'REPEAR')

        self.monet_db = json.load(os.getcwd() + '/photo_db.json')

    def check(self):
        # 检查源photos图库有无更新 检查md5值 若有更新 重新计算图片数据值
        list = os.listdir(self.photos_path) 
        #列出文件夹下所有的目录与文件
        md5s = []
        for i in range(0,len(list)):
            # 获取每个文件的md5,排序,相加再求md5
            path = os.path.join(rootdir,list[i])
            if os.path.isfile(path):
                md5s.append(GetFileMd5(path))
        md5s.soted()
        photos_md5s = GetStrMd5("".join(md5s))
        return photos_md5s == self.monet_db.get("md5")
                



    def photos_color_db():
        # 计算图片库的颜色值
        list = os.listdir(self.photos_path) 
        colors = {}
        for filename in lis:
            photo = Image.open(filename)
            width =photo.width
            height = photo.height
            # small_photo 压缩后图片
            small_photo = photo.resize((100, int(100*photo.height/photo.width)), Image.ANTIALIAS) 
            rgblist = small_photo.getdata()
            r = g = b = 0
            for rgb in list(rgblist):
                r += rgb[0]
                g += rgb[1]
                b += rgb[2]
            small_photo_color =  (int(r/len(rgblist)), int(g/len(rgblist)), int(b/len(rgblist)))
            colors[small_photo_color] = filename
        return colors

    def splits(self, x):
        # 传入一个图片类 把图片分割为若干小图片
        # x为横向张数 纵向按比例算
        photo = Image.open(self.target_path)
        width =photo.width
        hight = photo.height
        y = x * hight / width
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
  
    def similar():
        # 寻找相似的图片
        pass
    
    def split_joint(self, photos):
        # 拼接为一张大图
        pass     

    def run(self):
        check_md5 = self.check()
        if not check_md5:
            # 数据源有改动 另算
            pass

        photos = self.splits(self.width)
        photos = self.similar(photos)
        pho = self.split_joint(photos)



    def test(self):
        print(self.target_path)
        print(self.photos_path)
        print(self.width)
        print(self.hight)
        print(self.repear)

if __name__ == '__main__':
    a = Monet()
    a.test()
      
