#coding=utf-8
import paramiko
import threading
#import getpass
#passwd=getpass.getpass('Please input passwd:')
l=open('iplist')
log_file=open("log_file", "wb")
def work(ip,log_file):
    print 'Current IP '+ip
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        pkey='./ssh_key'  #本地密钥文件路径
        key=paramiko.RSAKey.from_private_key_file(pkey)
        ssh.connect(ip,22,'root',pkey=key,timeout=30)
#
        stdin, stdout, stderr = ssh.exec_command (" ls -l /root)
        for x in stdout.readlines():
            print x.strip("\n")
            log_file.write(ip.strip("\n")+' '+x.strip("\n")+' '+'\n')
        ssh.close()
    except:
        log_file.write(ip.strip("\n")+' not OK'+'\n')
        ssh.close()
try:
    ts=[]
    for i in l.readlines():

        t=threading.Thread(target=work,args=(i,log_file))
        t.start()
        while True:
        #判断正在运行的线程数量,如果小于5则退出while循环,
        #进入for循环启动新的进程.否则就一直在while循环进入死循环
            if(len(threading.enumerate()) < 60):
                break
        ts.append(t)
    for t in ts:
        t.join()
finally:
    print 'ending'
    log_file.close()
    l.close()