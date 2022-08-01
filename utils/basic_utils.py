import configparser
import os
import shutil
import webbrowser
import zipfile

from PyQt5.QtCore import QThread, pyqtSignal


def humanize_bytes(num: int, suffix='B') -> str:
    if num < 1024.0:
        return '%.1fB' % num
    for unit in ['B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def save_config_file(content: dict, config_class="DEFAULT"):
    config = configparser.ConfigParser()
    config[config_class] = content
    with open("./config.ini", "w") as f:
        config.write(f)


def read_config(key, config_class='DEFAULT'):
    config = configparser.ConfigParser()
    config.read("./config.ini")
    return config[config_class][key]


def open_url_in_browser(url):
    webbrowser.open(url, new=2)


def verify_mc(dir_path):
    for root, dirs, files in os.walk(dir_path):
        if ".minecraft" in dirs:
            return True
    return False


def verify_zip_is_mc(zip_path):
    dir_list = []
    zip_ref = zipfile.ZipFile(zip_path, 'r')
    for folder in zip_ref.namelist():
        if folder.endswith('/'):
            dir_list.append(os.path.basename(os.path.normpath(folder)))

    if ".minecraft" in dir_list:
        return True
    else:
        return False


class UnzipThread(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super(UnzipThread, self).__init__()
        self.zip_path = ""
        self.save_path = ""
        self.zipref = None

    def run(self):
        if os.path.exists(self.save_path):
            shutil.rmtree(self.save_path)
        os.mkdir(self.save_path)
        with zipfile.ZipFile(self.zip_path, 'r') as self.zipref:
            self.zipref.extractall(os.path.join(self.save_path))
        self.finished.emit()


if __name__ == "__main__":
    print(verify_zip_is_mc("C:\\Users\\alairack\Downloads\\DG5451412_x64.zip"))