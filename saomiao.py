import socket
import re 
import queue
import threading
from optparse import OptionParser

tishifu='''
            提示:
                python saomiao.py 127.0.0.1
                python saomiao.py 127.0.0.1 -p 21,80,3389
                python saomiao.py 127.0.0.1 -p 21,80,3389 -n 50

'''
print(tishifu)
que=queue.Queue()

class scan(object):

    def __init__(self,user_ip,prot,xianc=100):#构造函数中传入参数
        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", user_ip):#正则匹配
            self.user_ip=user_ip#指定ip，传入的ip赋值给user_ip
            print ("IP 输入正确")
        else:
            print ("IP 输入有误")
            exit()
        self.xianc=xianc
        self.prot=prot

    def panduanduankou(self):#添加一个判断输入端口号函数
        if self.prot == 65535:
            for i in range(0,65536):
                que.put(i)  #将获取的端口号加入列表当中
        else:
            for i in self.prot:
                if int(i)<0 or int(i)>65535:
                    print("端口输入错误请重新输入")
                    exit()
                que.put(i)
        try:
            print("正在扫描",self.user_ip)
            kunsha_xianchenchi=[]
            for i in range(0,int(self.xianc)):#将传入进来的线程进行int类型转换
                th = threading.Thread(target=self.run,args=())#target为目标=run函数中的return值
                kunsha_xianchenchi.append(th)
            for i in kunsha_xianchenchi:
                i.setDaemon(True)#设置守护进程判断进程是否为True
                i.start()#调用判断端口函数
            que.join()#阻塞主线程
            print("扫描完成")
        except EnvironmentError as e:
            print(e)
        except KeyboardInterrupt:
            print("用户退出扫描")

    def run(self):
        while not que.empty():#判断que.put()中有没有值
            prot=int(que.get())
            #print(port)
            if self.saomiao(prot):
                banner=self.banner(prot)#banner中存储着return返回来的banner函数的值
                if banner:
                    print("端口号为：%s"%prot,"具体参数为：%s"%banner)
                else:
                    print("端口号为：%s"%prot)
            que.task_done()

    def saomiao(self,prot):
        try:
            kunsha_sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            kunsha_sk.settimeout(0.5)
            if kunsha_sk.connect_ex((self.user_ip,prot))==0:
                return True
            else:
                return False
        except Exception as e:#防止报错的写法
            print("saomiao:",e)
            pass
        except KeyboardInterrupt :
            print("退出扫描")
            exit()
        finally:
            kunsha_sk.close()

    def banner(self,prot):
        try:
            kunsha_sk1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            kunsha_sk1.settimeout(0.5)
            kunsha_sk1.connect_ex((self.user_ip,prot))
            kunsha_sk1.send("hellow\r\n".encode("utf-8"))
            return kunsha_sk1.recv(2048).decode("utf-8")
        except Exception as e:
            pass
        finally:
            kunsha_sk1.close()

parser = OptionParser()

parser.add_option("-p","--prot",action = "store",type = "string" ,dest = "prot",help="所有要扫描的端口默认为所有端口 ")
parser.add_option("-n","--num",action="store",type="int",dest="xianc",help="线程默认为100")
(option,args)= parser.parse_args()
if option.prot ==None and option.xianc==None and len(args)==1:
    scanner=scan(args[0],65535)
    scanner.panduanduankou()
elif option.prot != None and option.xianc ==None and len(args)==1:
    prot = option.prot.split(",")
    scanner=scan(args[0],prot)
    scanner.panduanduankou()
elif option.prot == None and option.xianc !=None and len(args)==1:
    scanner=scan(args[0],65535,option.xianc)
    scanner.panduanduankou()
elif option.prot!=None and option.xianc!=None and len(args)==1:
    prot=option.prot.split(",")
    scanner=scan(args[0],prot,option.xianc)
    scanner.panduanduankou()
else:
    parser.print_help()