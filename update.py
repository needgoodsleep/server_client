import shutil
import sys
import requests
import os
import time
import zipfile
import subprocess
import urllib3
import urllib.request

import wget
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication, QDialog, QHBoxLayout, QProgressBar, QVBoxLayout

from app_config import AppConfig

release_info_json = "https://raw.githubusercontent.com/needgoodsleep/server_client/master/data/release.json"


def judge_update():
    try:
        info = requests.get(release_info_json).json()
    except Exception:
        return
    latest_version = info['latest_version']

    download_url = "https://gd-cowtransfer.cdn.cowtransfer.com/cowtransfer/cowtransfer/15732/00edaaf6-8c17-49ed-b80c-8342093ada6820362677.zip?response-content-disposition=attachment%3B%20filename%3DMinecraft%20Earth%20beta1.01.zip%3Bfilename*%3Dutf-8%27%27Minecraft%20Earth%20beta1.01.zip&auth_key=1659150598-879d2037889e4012b725ad496d778ff4-0-9f525235f3a2c6e0b6a85fb00c6275be&user_id=1020724947983813600&biz_type=1&channel_code=COW_CN_WEB&business_code=COW_TRANSFER"#info['download_url']
    update_log = info["update_log"]
   # path = '../pyweather.exe'
    #mtime = os.stat(path).st_mtime
    #modify_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(mtime))
    current_version = AppConfig.app_version
    if latest_version > current_version:
        update_dialog = UpdateDialog(latest_version, update_log)
        update_dialog.setWindowModality(Qt.ApplicationModal)
        update_dialog.resize(300, 200)
        update_dialog.exec_()
        update_file_path = download(download_url)
        #install(update_file_path, exist_file_path)
    else:
        print("new")


def download_json(url):
    json_path = urllib.request.urlretrieve(url)
    return json_path[0]


def get_version():
    api = "https://api.github.com/repos/alairack/learngit/releases/latest"
    info = requests.get(api).json()
    update_version = info["tag_name"]
    return update_version


def download(url):
    response = requests.get(url)
    zip_path = "./client_new_version"
    unzip_path = "./update_folder"
    with open(zip_path, 'wb') as file:
        file.write(response.content)
        file.flush()
    f = zipfile.ZipFile(zip_path)
    f.extractall(unzip_path)
    f.close()
    update_file_path = unzip_path + r'\pyweather'
    update_file_path = os.path.dirname(os.path.abspath(update_file_path))
    return update_file_path


def install(update_file_path, exist_file_path):
    b = open("../update.bat", 'w')
    templist = "@echo off\n"
    templist = templist + 'taskkill /f /im "pyweather.exe"\n'
    templist = templist + "ping -n 5 127.1>nul\n"   # sleep 4s
    update_file_path = update_file_path + r'\pyweather'
    templist = templist + f"copy {update_file_path} {exist_file_path}\n"
    exe_path = exist_file_path + r'\pyweather.exe'
    templist = templist + f'start {exe_path}\n'
    templist = templist + 'exit'
    b.write(templist)
    b.close()
    path = os.path.abspath('..')
    path = path + '/update.bat'
    subprocess.Popen(path, shell=True)


def install2(update_path, exist_path):
    os.rename(exist_path + r'\pyweather.exe', exist_path + r'\pyweather.exe.temp')
    shutil.copy(update_path, exist_path)
    exe_path = exist_path + r'\pyweather.exe'
    os.execv(exe_path, [exe_path])


class UpdateDialog(QDialog):
    def __init__(self, latest_version, update_info):
        super(UpdateDialog, self).__init__()
        self.latest_version = latest_version
        self.update_info = update_info
        self.initUI()

    def initUI(self):
        self.setWindowTitle("正在更新")

        self.vbox_layout = QVBoxLayout()
        self.setLayout(self.vbox_layout)

        self.label_title = QtWidgets.QLabel(f"正在更新至{self.latest_version}版本, 请勿关闭软件")
        self.update_log_label = QtWidgets.QLabel(self.update_info)
        self.process_bar = QProgressBar()
        self.process_bar.setMaximum(100)
        self.process_bar.setMinimum(0)

        self.vbox_layout.addWidget(self.label_title)
        self.vbox_layout.addWidget(self.update_log_label)
        self.vbox_layout.addWidget(self.process_bar)



if __name__ == "__main__":
    download_json("https://raw.githubusercontent.com/needgoodsleep/server_client/master/data/release.json")