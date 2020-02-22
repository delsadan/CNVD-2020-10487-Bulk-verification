# CNVD-2020-10487(CVE-2020-1938)批量验证脚本
批量脚本，基于@YDHCUI的POC文件制作，批量且可以自动截图，方便复核

## 一、环境准备

虚拟环境请用conda安装（自行百度miniconda安装），因为POC用的python2，所以要建一个python2环境，一个python3环境

### python2(POC运行环境)：
    conda create -n python2 python=python2.7
    
### python3(本脚本运行环境):
    conda create -n biubiubiu python=python3.7
    pip install pywin32
    pip install pyqt
    pip install loguru
无法导入win32gui， 参考：https://stackoverflow.com/questions/3956178/cant-load-pywin32-library-win32gui

必须在cmd环境下运行，否则截图不正常！

### usage：
    · 设置下面的TomcatLFI_path路径
    · conda activate biubiubiu
    · cd 到cmd.py所在文件夹目录
    · python cmd.py
其他详细使用说明见cmd.py

## 二、效果
根据`Getting resource`是否存在于返回的结果字符串判断漏洞

有漏洞的截图会以jpg格式保存，不存在就是png。

脚本所在目录会自动生成一个保存结果的txt
