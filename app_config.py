def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner()


@singleton
class AppConfig(object):
    app_name = "西瓦大陆工具"
    app_version = "0.1.0"  # 版本号必须为3位

    game_package_name = "Minecraft Earth.zip"
    game_package_download_url = "https://cowtransfer.com/s/73da937392af40"