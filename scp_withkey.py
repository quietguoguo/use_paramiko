#coding=utf-8
import paramiko
import threading
import os


local_file=raw_input('Please input local file name:')
remote_file=raw_input('Please input remote file name,the whole name include path and name:')

l=open('iplist')
log_file=open("log_file", "wb")


if os.path.isfile(local_file):
    print local_file+' is file'
else:
    print local_file+' is not file'

def work(ip,log_file):
    try:
        print ip
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        pkey='./ssh_key'  #本地密钥文件路径
        key=paramiko.RSAKey.from_private_key_file(pkey) #有解密密码时,
        ssh.connect(ip,22,'root',pkey=key,timeout=25)
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        sftp.put(local_file,remote_file)
        sftp.close()
        ssh.close()
    except Exception as e:
        print e
try:
    ts=[]
    for i in l.readlines():
        t=threading.Thread(target=work,args=(i,log_file))
        t.start()
        while True:
        #判断正在运行的线程数量,如果小于5则退出while循环,
        #进入for循环启动新的进程.否则就一直在while循环进入死循环
            if(len(threading.enumerate()) < 50):
                break
        ts.append(t)
    for t in ts:
        t.join()
finally:
    print 'ending'
    log_file.close()
    l.close()