import configparser # ConfigParser
import os
import json
from PIL import Image
from common import GetFileMd5, GetStrMd5, width_size, Base, PHOTO_SUFFIX

class ClearPhoto(Base):
    """清洗函数"""
    def repeats(self):
        """
        清洗重复和比例
        1 用md5s清洗掉重复照片
        2 用clear_photos 统计照片的长宽比例，取最多的长宽比的照片作为clear_photos_list 其他的放弃
        """
        p_list = os.listdir(self.photos_path)
        #列出文件夹下所有的目录与文件
        md5s = []
        clear_photos = {}
        print("清洗分类")
        alls = len(p_list)
        for i in range(alls):
            # 获取每个文件的md5,排序,相加再求md5
            # 检查后缀
            print(float(i)/alls)
            suffix = p_list[i].split('.')[-1]
            if suffix not in PHOTO_SUFFIX:
                continue
            path = os.path.join(self.photos_path,p_list[i])
            try:
                photo = Image.open(path)
            except:
                continue
            if os.path.isfile(path):
                _md5 = GetFileMd5(path)
                if _md5 not in md5s:
                    md5s.append(_md5)

                    width = photo.width
                    hight = photo.height
                    keys = str(round(width/hight, 2))
                    if keys not in clear_photos:
                        clear_photos[keys] = []
                    clear_photos[keys].append(p_list[i])
        # 计算所有图片的MD5 下次方便检查
        md5s.sort()
        photos_md5s = GetStrMd5("".join(md5s))
        self.db["photos_md5"] = photos_md5s
        self.save_db(self.db)

        max_key = ''
        counts = 0
        print(clear_photos)
        for keys in clear_photos:
            if len(clear_photos[keys]) > counts:
                max_key = keys
                counts = len(clear_photos[keys])
        clear_photos_list = clear_photos[max_key]
        return clear_photos_list

    def MiniPhotos(self, clear_photos_list):
        """计算缩略图，保存到miniphoto下"""
        print("计算缩略图。。。")
        alls = len(clear_photos_list)
        i = 0
        for photo_name in clear_photos_list:
            suffix = photo_name.split('.')[-1]
            if suffix not in PHOTO_SUFFIX:
                continue
            print(float(i)/alls)
            i += 1
            path = os.path.join(self.photos_path,photo_name)
            photo = Image.open(path)
            width = photo.width
            height = photo.height
            mini_photo = photo.resize((width_size, int(width_size * photo.height / photo.width)), Image.ANTIALIAS)
            mini_photo_path = os.path.join(self.photos_path,".miniphoto")
            if not os.path.exists(mini_photo_path):
                os.makedirs(mini_photo_path)
            mini_photo.save(os.path.join(mini_photo_path, photo_name))

    def run(self):
        clear_photos_list = self.repeats()
        self.MiniPhotos(clear_photos_list)
        print("clear done")

if __name__ == "__main__":
    pass
