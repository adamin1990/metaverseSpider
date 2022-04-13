# -*- coding: utf-8 -*-
# Author: MindBin

import os
# 导入os模块
command_list = 'pip list'
command_install = 'pip install '
data = os.popen(command_list)
info = data.readlines()  #读取命令行的输出到一个list
# 删除表头信息
del info[0]
del info[0]
for line in info:  #按行遍历
    # 用" "分割每行，列表的第一个就是包名
    package = line.split(" ")[0]
    print("",end="")
    print("\033[1;32;40m%s\033[0m"%("正在检查更新"+package))
    os.system(command_install+package+" --upgrade")
print("更新完毕")

