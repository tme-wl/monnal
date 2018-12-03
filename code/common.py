import os
import hashlib

def GetFileMd5(filename):
    """获取文件的md5"""
    if not os.path.isfile(filename):
        return None
    myhash = hashlib.md5()
    f = file(filename,'rb')
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
    m0.update(src)
    return m0.hexdigest()
