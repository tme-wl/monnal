import configparser
import os
import json
import hashlib

VERSION = 1.0

# mini图片的像素
width_size = 100

PHOTO_SUFFIX = ["JPG", "PNG", 'jpg', 'png', 'jpeg']
"""
photo_db = {
    "version": 1.0
    "photo_db": {
        "name": [],
    }

}
"""
def GetFileMd5(filename):
    """获取文件的md5"""
    if not os.path.isfile(filename):
        return None
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def GetStrMd5(src):
    """获取字符串的md5"""
    m0=hashlib.md5()
    m0.update(src.encode('utf-8'))
    return m0.hexdigest()

def core(photo):
        """
        一张照片的核心算法
        photo为一个PILLOW对象
        返回计算结果后的值
        """
        rgblist = photo.getdata()
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

class Base(object):
    """
    处理基础使用环境
    """
    def __init__(self):
        # 读取配置
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), "config.ini"))
        # 目标图片路径
        self.target_path = config.get('path', 'TARGET_PHOTO')
        # 图片库路径
        self.photos_path = config.get('path', 'PHOTOS')
        # 设置宽高
        self.width = int(config.get('size', 'WIDTH'))
        # 是否重复
        self.repeat = config.get('other', 'REPEAT')
        self.target_save_path = config.get("path", "TARGET_SAVE_PATH")

        self.db_path = os.path.join(os.getcwd(), "photo_db.json")
    
    # def init_db(self):
        self.db = dict()
        with open(self.db_path, 'r') as db_fp:
            self.db = json.load(db_fp)
        
        self.mini_photo_list = os.path.join(self.photos_path, ".miniphoto")

        self.version = VERSION
        
    def save_db(self, db):
        with open(self.db_path, "w") as db_fp:
            json.dump(db, db_fp)
        
    def get_db(self):
        self.db = dict()
        with open(self.db_path, 'r') as db_fp:
            self.db = json.load(db_fp)
        return self.db
