import ConfigParser
import os
import json
from PIL import Image
from common import GetFileMd5, GetStrMd5


class ClearPhoto(object):
    """清洗函数"""

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

    def Repeat(self):
        """清洗重复和比例"""
        list = os.listdir(self.photos_path)
        #列出文件夹下所有的目录与文件
        md5s = []
        clear_photos = {}
        for i in range(0,len(list)):
            # 获取每个文件的md5,排序,相加再求md5
            path = os.path.join(self.photos_path,list[i])
            if os.path.isfile(path):
                _md5 = GetFileMd5(path)
                if _md5 not in md5s:
                    md5s.append(_md5)
                    photo = Image.open(self.target_path)
                    width = photo.width
                    hight = photo.height
                    keys = width + '_' + hight
                    if keys not in clear_photos:
                        clear_photos[keys] = []
                    clear_photos[keys].append(list[i])
        max_key = ''
        counts = 0
        for keys in clear_photos:
            if len(clear_photos[keys]) > counts:
                max_key = keys
                counts = len(clear_photos[keys])

        clear_photos_list = clear_photos[max_key]
        return clear_photos_list

    def MiniPhotos(self, clear_photos_list):
        for photo in clear_photos_list:
            width = photo.width
            height = photo.height
            mini_photo = photo.resize((100, int(100 * photo.height / photo.width)), Image.ANTIALIAS)
            mini_photo.save(photo)


        return photos_md5s == self.monet_db.get("md5")