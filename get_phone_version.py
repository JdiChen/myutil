"""
6801 daily auto download and upgrede power on
"""
import os
import subprocess
import sys
sys.path.append('../config')
from config.path_config import GET_VERSION_PATH

from util import depend

import time
from ftplib import FTP
from zipfile import ZipFile
import datetime
from util.depend import get_logger, read_yaml, get_all_adb_devices

log = get_logger('update')


def get_date(before_day=0):
    day = datetime.date.today() - datetime.timedelta(days=before_day)
    return day.strftime('%Y%m%d')



class PhoneVersion:
    config = read_yaml(GET_VERSION_PATH)
    # sn = 'f28f92ad'
    sn = config['sn']
    server_ip = config['server_ip']
    user = config['user']
    pwd = config['pwd']
    ftp = None
    # name_date = strftime('%Y%m%d', localtime())
    # name_date
    # 项目daily目录路径
    remote_version_path = config['remote_version_path']
    # 远程daily版本目录名称
    remote_dir_name = None
    # 本地下载目录
    local_path = config['local_path']
    # 本地下载的文件路径
    local_file_path = None
    userdebug_path = None
    download_path = None
    download_filename = None
    over_time = config['over_time']

    def get_ftp_server(self):
        """连接ftp"""
        self.ftp = FTP(self.server_ip)
        try:
            log.info('connect ftp')
            self.ftp = FTP(self.server_ip)
            self.ftp.login(self.user, self.pwd)
            log.info('ftp connect success')
        except Exception as e:
            log.info('connect ftp fail')
            raise e
        self.ftp.encoding = 'utf-8'


    def _get_remote_dir_name(self):
        # 切换到远程daily目录,如果检测到版本目录，就跳出
        self.ftp.cwd(self.remote_version_path)
        # 有两个版本时的选择？  会选择最后一个
        while True:
            # 超过每天的9.30就不执行了
            log.info('----------------------------')
            if time.ctime()[-13:-5] > self.over_time:
                log.info('over 8.30')
                sys.exit(1)
            daily_dir_name = None
            for i in self.ftp.nlst():
                if get_date() in i:
                    daily_dir_name = i
            # daily_dir_name = self.ftp.nlst()[-1]
            if daily_dir_name is None:
                log.info('can not find daily version dir,retry after 10 min')
                time.sleep(60 * 10)
                self.get_ftp_server()
                continue
            log.info(f"daily_dir_name is {daily_dir_name}")
            if get_date() in daily_dir_name:
                # or get_date(before_day=1) in daily_dir_name \
                # or get_date(before_day=2) in daily_dir_name:
                self.remote_dir_name = daily_dir_name
                log.info(f'remote path name is {self.remote_dir_name}')
                break
            # else:
            #     log.info('can not find daily version dir,retry after 5 min')
            #     # FTP服务器会有超时检测
            #     time.sleep(60 * 5)
            #     continue

    def _is_exist_local_daily_version(self):
        for i in os.listdir(self.local_path):
            if i.endswith('.zip'):
                continue
            if get_date() in i:
                log.info('the daily version already exists')
                return True
        log.info('need download version')
        return False

    def _get_download_path(self):
        self._get_remote_dir_name()
        # 取得 userdebug 目录的完整路径
        self.userdebug_path = self.remote_version_path + '/' + self.remote_dir_name + '/' + 'userdebug' + '/'

        log.info(self.userdebug_path)
        while True:
            if time.ctime()[-13:-5] > self.over_time:
                log.info('userdebug path not found over 8.30')
                sys.exit(1)
            try:
                self.ftp.cwd(self.userdebug_path)
                break
            except Exception as e:
                log.info(e.__str__())
                log.info("wait 1 min and try it")
                time.sleep(60)
                continue

        for i in self.ftp.nlst():
            if i.endswith('USERDEBUG_UPGRADE.zip'):
                self.download_path = self.userdebug_path + i
                self.download_filename = i
                with open('E:\PythonProject\Q6801_AUTO_TEST\send_mail\phone_version.txt','w') as f:
                    f.write(self.download_filename)
        log.info(f'download_filename is {self.download_filename}')
        self.local_file_path = os.path.join(self.local_path, self.download_filename)

    def _download_version(self):
        with open(self.local_file_path, 'wb') as f:
            log.info(f'down load file path is {self.download_path}')
            log.info('正在下载...')
            try:
                self.ftp.retrbinary('RETR ' + self.download_path, f.write, 1024)
                log.info('下载完成')
            except Exception as e:
                log.info('下载失败')
                raise e

    def _unzip(self):
        zip_file = ZipFile(self.local_file_path, 'r')
        unzip_path = self.local_path
        log.info('正在解压......')
        zip_file.extractall(unzip_path)
        zip_file.close()
        log.info('解压完成')

    def _updata(self):
        # path = r'F:\PhoneVersion\AutoTest\Q6501_SFT656128_V1.0.33_20200904-1-userdebug'
        path = os.path.join(self.local_path, os.path.splitext(self.download_filename)[0])
        log.info(f'after unzip paht is {path}')
        sn = self.sn

        try:
            result = get_all_adb_devices()
            assert sn in result, 'can not find %s,the result is %s' % (sn, result)
            os.system('adb -s %s reboot edl' % sn)
            log.info('ent er edl sleep 10s')
        except Exception as e:
            log.info('no device,may be the device is in edl mode,try it')
            log.info(e)

        time.sleep(10)
        qfil_path = r'E:\QualCommTools\QPST\bin\QFIL.exe'
        # 注意每一行最后都应该有空格
        cmd = '%s ' \
              '-mode=3 ' \
              '-downloadflat ' \
              '-com=7 ' \
              '-switchtofirehosetimeout=50 ' \
              '-resettimeout=500 ' \
              '-resetdelaytime=5 ' \
              '-resetafterdownload=true ' \
              '-devicetype=UFS ' \
              '-programmer=true;%s\prog_firehose_ddr.elf ' \
              '-searchpath=%s ' \
              '-rawprogram="rawprogram_upgrade0.xml,rawprogram_upgrade1.xml,rawprogram_upgrade2.xml,rawprogram_upgrade3.xml,rawprogram_upgrade4.xml,rawprogram_upgrade5.xml" ' \
              '-patch="patch0.xml,patch1.xml,patch2.xml,patch3.xml,patch4.xml,patch5.xml"' % (qfil_path, path, path)
        # cmd = 'ping 192.168.0.1'
        log.info('updata start')
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        start_time = time.time()
        while time.time() - start_time < 60*15:
            line = str(out.stdout.readline(),encoding='utf8')[:-2]
            log.info(line)
            if 'Download Fail:' in line:
                raise ValueError('updata fail ')
            if 'Download Succeed' in line:
                log.info('Download Succeed')
                break
            # time.sleep(1)
        out.wait(60*10)
        log.info('updata done')

    def start_updata(self):
        self.get_ftp_server()
        # self._get_remote_dir_name()
        self._get_download_path()
        if not self._is_exist_local_daily_version():
            self._download_version()
            self._unzip()
        self._updata()
        self.ftp.close()

    def check_version(self):
        log.info('start chcek version,wait the phone powered on')
        start_time = time.time()
        while True:
            if time.time() - start_time > 60 * 10:
                log.info('power on is timeout 10min,pleses check the device')
                break
            line = depend.shell(self.sn, 'dumpsys window | grep mCurrentFocus')
            # log.info(line)
            if 'com.google.android.setupwizard' in line:
                log.info('already show google setupwizard')
                log.info('power on done')
                # 设置屏幕长亮
                depend.shell(self.sn, 'svc power stayon true')
                log.info(f'the version is {depend.shell(self.sn, "getprop ro.vendor.build.version.incremental")}')
                break
            time.sleep(1)


if __name__ == '__main__':
    up = PhoneVersion()
    # up.get_ftp_server()

    up.start_updata()
    up.check_version()
    # log.info(up.shell('dumpsys window | findstr mCurrentFocus'))
