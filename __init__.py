# coding:utf-8
import os
import hashlib
import time
import logging
import logging.handlers
import filesvn.client

allfile = []

def init_logger(log_file):
    dir_path = os.path.dirname(log_file)
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except Exception as e:
        pass
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=100 * 1024 * 1024, backupCount=10,encoding='utf-8')
    fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger_instance = logging.getLogger('logs')
    logger_instance.addHandler(handler)
    logger_instance.setLevel(logging.DEBUG)
    return logger_instance

# ---------------------
# logging 日志代码
# 来自 听雪声的春天 的CSDN 博客 ，全文地址请点击：https://blog.csdn.net/grs294845170/article/details/78800707?utm_source=copy

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def getallfile(path):
    allfilelist = os.listdir(path)
    for file in allfilelist:
        filepath = os.path.join(path, file)
        # 判断是不是文件夹
        if os.path.isdir(filepath):
            getallfile(filepath)
        allfile.append(filepath)
    return allfile

if __name__ == '__main__':

    path = "W:\SvnFolder"
    mylog = init_logger('./result.log')

    md5_list = []
    file_name_list=[]

    with open('filemd5.txt','r') as fr:
        content=fr.read()
        md5_list=content.split('-')
    print(md5_list)
    serverip='192.168.1.100'
    serverport=2333

    while True:
        allfiles = getallfile(path)
        for item in allfiles:
            filepath=item
            filemd5=GetFileMd5(item)
            # print(filepath)
            # print(filemd5)
            if filemd5 not in md5_list:
                print(filepath)
                print(filemd5)
                mylog.info(u'新文件，准备传送')
                mylog.info(filemd5)
                mylog.info(filepath)
                print('新文件，准备传送')
                # Client=filesvn.client.Client()
                filesvn.client.Client(serverip,serverport).transferFile(filepath)
                print(md5_list)
                md5_list.append(str(filemd5))
                with open('filemd5.txt','w+') as fw:
                    fw.write('-'.join(md5_list))
                file_name_list.append(filepath)
        time.sleep(1)
