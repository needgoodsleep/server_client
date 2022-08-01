class DownloadGameDialog(QDialog):
    def __init__(self):
        super(DownloadGameDialog, self).__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("下载游戏客户端")
        self.vbox_layout = QVBoxLayout()

        self.setLayout(self.vbox_layout)

        self.label_download_progress = QLabel()
        self.btn_stop = QPushButton("停止下载")
        self.btn_stop.clicked.connect(self.stop_download)

        self.vbox_layout.addWidget(self.label_download_progress)
        self.vbox_layout.addWidget(self.btn_stop)

    def stop_download(self):
        if self.download_manager.cmd_object:
            self.download_manager.cmd_object.terminate()

    def start_download(self):
        self.download_manager = DownloadManager()
        self.download_manager.run()

        while self.download_manager.cmd_object.poll() is None:
            package_path = f"./{AppConfig.game_package_name}"
            if os.path.exists(package_path):
                file_size = os.stat(package_path).st_size
            else:
                file_size = 0
            self.label_download_progress.setText("已下载:" + basic_utils.humanize_bytes(file_size))

        self.label_download_progress.setText("下载已停止")
