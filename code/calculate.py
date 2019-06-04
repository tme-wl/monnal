import os
import json
from PIL import Image
from common import core as photo_core, Base, PHOTO_SUFFIX


class Calculate(Base):
    """清洗函数"""

    def core(self, photo):
        """
        一张照片的核心算法
        photo为一个PILLOW对象
        返回计算结果后的值
        """
        return photo_core(photo)

    def color_reckon(self):
        mini_list = os.listdir(self.mini_photo_list)
        photo_db = {
            "version": self.version,
            "photo_db":{}
        }
        for mini_photo_name in mini_list:
            suffix = mini_photo_name.split('.')[-1]
            if suffix not in PHOTO_SUFFIX:
                continue
            path = os.path.join(self.mini_photo_list,mini_photo_name)
            photo = Image.open(path)
            photo_db["photo_db"][mini_photo_name] = self.core(photo)
        self.db.update(photo_db)
        self.save_db(self.db)


    def run(self):
        self.color_reckon()

        
if __name__ == "__main__":
    obj = Calculate()
    print("计算图片数据")
    obj.color_reckon()
    print("计算完成")



