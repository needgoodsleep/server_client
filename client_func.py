import os
import subprocess
import sys
import time

from PyQt5.QtCore import QThread

from app_config import AppConfig


class DownloadManager(object):
    def __init__(self):
        self.cmd_object = None

    def run(self):
        self.cmd_object = subprocess.Popen(AppConfig.game_package_download_cmd)


if __name__ == "__main__":
    pass