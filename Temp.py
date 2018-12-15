#-*-encoding:utf-8-*-
  
import  socket
import  os
import  sys
import  math
import  time
  
def  progressbar(cur,  total):
        percent  =  '{:.2%}'.format(float(cur)  /  float(total))
        sys.stdout.write('\r')
        sys.stdout.write("[%-50s]  %s"  %  (
                                                        '='  *  int(math.floor(cur  *  50  /  total)),

                                                        percent))

        sys.stdout.flush()
  
def  getFileSize(file):
        file.seek(0,  os.SEEK_END)
        fileLength  =  file.tell()
        file.seek(0,  0)
        return  fileLength
  
def  getFileName(fileFullPath):
        index  =  fileFullPath.rindex('\\'.encode())
        if  index  ==  -1:
                return  fileFullPath  
        else:
                return  fileFullPath[index+1:]
  
def  transferFile():
        fileFullPath  =  'W:\SvnFolder\__init__.py'
        if  os.path.exists(fileFullPath):

                timeStart  =  time.clock()
                file  =  open(fileFullPath,  'rb')
                fileSize  =  getFileSize(file)

                client  =  socket.socket(socket.AF_INET,  socket.SOCK_STREAM)

                client.connect((targetHost,  targetPort))
                #  send  file  size
                client.send(str(fileSize).encode())
                response  =  client.recv(1024)
                #  send  file  name

                client.send(getFileName(fileFullPath.encode()))
                response  =  client.recv(1024)
                #  send  file  content
                sentLength  =  0
                while  sentLength  <  fileSize:
                        bufLen  =  1024
                        buf  =  file.read(bufLen)

                        client.send(buf)
                        sentLength  +=  len(buf)
                        process  =  int(float(sentLength)  /  float(fileSize)  *  100)
                        progressbar(process,  100)
                client.recv(1024)
                file.close()

                timeEnd  =  time.clock()
                print("\r\nFinished,  spent  %d  seconds" % (timeEnd - timeStart))
        else:
            print("File  doesn't  exist")


targetHost  =  '192.168.1.100'
targetPort  =  2333

  
while  True:

        transferFile()
#
# ---------------------
#
# 本文来自 远行的风 的CSDN 博客 ，全文地址请点击：https://blog.csdn.net/qwertyupoiuytr/article/details/65667552?utm_source=copy