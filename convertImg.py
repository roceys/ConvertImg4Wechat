import os
import binascii
import datetime

"""将目录下的文件按照最后修改时间顺序升序排列"""
def getFileList(path):
    dirLists = os.listdir(path)
    if not dirLists:
        return
    else:
        dirLists = sorted(dirLists,key=lambda f: os.path.getmtime(os.path.join(path, f)))
        print('文件数量：{}个\n最新文件名为<{}>'.format(len(dirLists),dirLists[-1]))
        return dirLists

"""获取文件的16进制前多少位，如4位、6位"""
def getFileHex(path,step):
    fileName = getFileList(path)[-1]
    fileData = open(path+'\\'+fileName,'rb')
    hexstr = binascii.b2a_hex(fileData.read())
    hex = str(hexstr)[2:step+2] #获取16进制前多少位，4或6位
    print('dat十六进制文件头前{}位为:{}'.format(step,hex))
    return hex

"""
16进制异或运算
"""
def Xor(dir):
    hex2 = int(getFileHex(dir, 2), 16)
    """先取前四位，再取前两位，运算结果一致才算获得解密偏移量"""
    jpg = int('ff', 16)  # jpeg文件头16进制为ffd8ff
    png = int('89504E47', 16)  # png文件头16进制为89504E47
    gif = int('47494638', 16)  # gif文件头16进制为47494638
    return hex(hex2 ^ jpg)

def convertImg(file,fileName,step):
    dat = open(file, "rb")
    out='C:\\img\\'+'20191224晚剧本杀'+fileName+'.jpg'
    newFile = open(out, "wb")

    for cur in dat:
        for hex in cur:
            originHex = hex ^ step
            newFile.write(bytes([originHex]))

    dat.close()
    newFile.close()
    print('转换完成文件：{}'.format(out))


def main(dir,date1,date2):
    files = os.listdir(dir)
    format_ = '%Y-%m-%d %H:%M:%S'
    step = int(Xor(dir),16)
    print('十进制偏移量为{}'.format(step))
    i = 0
    for fn in files:
        _path = os.path.join(dir, fn)
        _time = os.path.getmtime(_path)
        dt_time = datetime.datetime.fromtimestamp(_time).strftime(format_)

        if dt_time < date1 or dt_time > date2:
            continue

        if not os.path.isdir(_path):
            print('当前文件: {}' .format(_path))
            convertImg(_path,fn,step)
            i+=1

    print('总计转换图片文件{}个'.format(i))

"""
自动判断微信PC客户端加密文件dat后缀格式图片16进制文件头
自动计算图片文件解密偏移量并转换为可用的图片文件（jpg|png|gif）
可指定具体微信图片缓存本地的日期时间范围进行转换图片提取

JPG文件头16进制为FFD8FF
PNG文件头16进制为89504E47
GIF文件头16进制为47494638

ROCEYS.CN
2019-12-26 01:16:00
"""

if __name__=="__main__":
    dir = r'F:\手机备份\微信备份\WeChat Files\togosb\FileStorage\Image\2019-12'
    d1 = '2019-12-25 20:12:00'
    d2 = '2019-12-25 20:20:59'
    main(dir,d1,d2)
