import os
import time

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog, QProgressBar, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, Qt, QtGui, QtWidgets
from functools import partial

from app_config import AppConfig
from client_func import DownloadManager
from utils import basic_utils
import zipfile

from utils.basic_utils import UnzipThread


class StartWidget(QWidget):
    def __init__(self):
        super(StartWidget, self).__init__()
        self.install_page = InstallGameDialog()
        self.initUI()

    def initUI(self):
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)

        self.logo = QPixmap("D://logo.ico")
        self.label = QLabel()
        self.label.setPixmap(self.logo)
        self.vlayout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)
        self.vlayout.addLayout(self.grid_layout)

        self.btn_download_package = CustomButton("下载游戏客户端")
        self.grid_layout.addWidget(self.btn_download_package)
        self.btn_download_package.clicked.connect(partial(basic_utils.open_url_in_browser, AppConfig.game_package_download_url))

        self.btn_install_mc = CustomButton("安装MC")
        self.btn_install_mc.clicked.connect(self.install_game_package)
        self.grid_layout.addWidget(self.btn_install_mc)

        self.btn_update_mod = CustomButton("更新mod")
        self.grid_layout.addWidget(self.btn_update_mod)

        self.btn_open_game_dir = CustomButton("打开MC文件夹")
        self.btn_open_game_dir.clicked.connect(self.open_game_dir)

        self.grid_layout.addWidget(self.btn_open_game_dir)

    def install_game_package(self):
        self.install_page.setWindowModality(QtCore.Qt.ApplicationModal)
        self.install_page.show()
        self.install_page.resize(200, 100)

    def open_game_dir(self):
        try:
            game_save_path = basic_utils.read_config('game_save_path')
        except Exception:
            QMessageBox.warning(self, "警告", '你还没有安装过MC！')
        else:
            os.startfile(game_save_path)


class CustomButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(CustomButton, self).__init__(*args, **kwargs)
        self.custom_init()

    def custom_init(self):
        self.setMinimumHeight(50)


class InstallGameDialog(QDialog):
    def __init__(self):
        super(InstallGameDialog, self).__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("安装MC")

        self.grid_layout = QGridLayout()

        self.setLayout(self.grid_layout)

        self.label_tips = QLabel("请在网页中下载压缩包,\n下载完成后请选择压缩包路径")

        self.label_package_path = QLabel()

        self.choose_btn = QPushButton('选择MC压缩包')
        self.choose_btn.clicked.connect(self.choose_game_package)

        self.label_save_path = QLabel()
        self.choose_save_path_btn = QPushButton('选择MC保存路径')
        self.choose_save_path_btn.clicked.connect(self.choose_save_path)

        self.start_btn = QPushButton('开始安装')
        self.start_btn.clicked.connect(self.start_install)

        self.loading = QLabel(self)

        self.grid_layout.addWidget(self.label_tips, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.label_package_path, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.choose_btn, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.label_save_path, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.choose_save_path_btn, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.start_btn, 3, 0, 1, 2)

    def choose_game_package(self):
        path = os.path.join(os.path.expanduser('~'), 'downloads')
        file_name, file_type = QFileDialog.getOpenFileName(self, "选取MC压缩包", path,
                                                           '压缩文件(*.zip *.rar *.7z)')
        if file_name:
            if not basic_utils.verify_zip_is_mc(file_name):
                QMessageBox.warning(self, "警告", "你选取的压缩包里面没有MC！")
            else:
                self.label_package_path.setText(file_name)

    def choose_save_path(self):
        path = os.path.expanduser('~')
        dir_name = QFileDialog.getExistingDirectory(self, "选取MC存储路径", path, QFileDialog.ShowDirsOnly)
        if dir_name:
            self.label_save_path.setText(dir_name)

    def start_install(self):
        if self.label_save_path.text() and self.label_package_path.text():
            save_path = os.path.join(self.label_save_path.text(),
                                     os.path.basename(self.label_package_path.text()).split(".")[0])
            self.unzip_thread = UnzipThread()
            self.unzip_thread.finished.connect(self.install_finish)
            self.unzip_thread.save_path = save_path
            self.unzip_thread.zip_path = self.label_package_path.text()
            self.unzip_thread.start()

            self.start_btn.setEnabled(False)
            self.start_loading()

    def start_loading(self):
        self.grid_layout.addWidget(self.loading, 4, 1, 1, 1)
        self.loading_gif = QtGui.QMovie('res/loading.gif')
        self.loading.setMovie(self.loading_gif)
        self.loading_gif.start()

    def install_finish(self):
        basic_utils.save_config_file({'game_save_path': self.unzip_thread.save_path})
        self.loading_gif.stop()
        self.grid_layout.removeWidget(self.loading)
        self.start_btn.setEnabled(True)
        QMessageBox.information(self, "信息", '安装完成!')



