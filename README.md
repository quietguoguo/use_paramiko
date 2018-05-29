# use_paramiko
使用paramiko实现远程批量执行命令与scp

remote_withkey.py 为老版本，使用ssh_key免密登录，需要修改文件来制定具体的命令，仅作为一个脚本使用是可行的。

scp_withkey.py    为老版本，使用ssh_key免密登录，需要交互选择具体的文件。

2018-05-29 更新

remote.py 针对原有脚本进行修改。完成模块化处理，可以被其他程序引用。

示例：

import remote

cmd='hostname'

remote.remote(cmd)



也可以直接带参数在命令行中调用

示例： 

python remote.py hostname


注意在命令行中注意引号转义的问题 。如果不提供参数会报错。
