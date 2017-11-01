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
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        pkey='/root/.ssh/id_rsa'  #本地密钥文件路径
        key=paramiko.RSAKey.from_private_key_file(pkey)
        ssh.connect(ip,22,'root',pkey=key,timeout=60)
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        sftp.put(local_file,remote_file)
    except Exception as e:
        print e
    ssh.close()
    sftp.close()
try:
    ts=[]
    for i in l.readlines():
        t=threading.Thread(target=work,args=(i,log_file))
        t.start()
        while True:
            if(len(threading.enumerate()) < 15):
                break
        ts.append(t)
    for t in ts:
        t.join()
finally:
    print 'ending'
    log_file.close()
    l.close()