import ctypes
import sys

from PyQt5 import QtWidgets, QtGui

from app_config import AppConfig
from start_widget import StartWidget
from update import judge_update


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(AppConfig.app_name)
        self.resize(800, 600)

        self.tab_widget = TabWidget()
        self.setCentralWidget(self.tab_widget)


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super(TabWidget, self).__init__()

        main_tab = StartWidget()
        self.addTab(main_tab, "总览")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("alairack")
    app.setWindowIcon(QtGui.QIcon(":/icons/logo.ico"))
    main_window = MainWindow()
    main_window.show()
    judge_update()
    sys.exit(app.exec_())
