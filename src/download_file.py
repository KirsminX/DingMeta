import requests, time
from alive_progress import alive_bar

import error

"""
文件处理
"""


class File:
    def __init__(self, url: str, path: str):
        self.url = url
        self.path = path

    def download(self):
        url = self.url
        path = self.path
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise error.DownloadError(f"下载失败！原因：{e}")

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024 * 10  # 块大小设置为10KB

        progress_bar_style = {
            "title": f"下载「{path}」",
            "bar": "blocks",
            "stats": ""
        }

        start_time = time.time()
        with alive_bar(total_size // block_size, enrich_print=False, manual=True, **progress_bar_style) as bar:
            try:
                with open(path, 'wb') as file:
                    downloaded = 0
                    for data in response.iter_content(block_size):
                        current_time = time.time()
                        elapsed_time = current_time - start_time
                        file.write(data)
                        downloaded += len(data)
                        bar(downloaded / total_size)  # 更新进度条

                        if elapsed_time > 0:
                            speed = (downloaded / (1024 * 1024)) / elapsed_time  # 以MB/s为单位计算速度
                            bar.text(f'速度: {speed:.2f} MB/s')
            except Exception as e:
                raise error.DownloadError(f"下载失败！原因：{e}")
if __name__ == "__main__":
    # 测试
    app = File("https://cdn.aliyundrive.net/downloads/apps/desktop/aDrive-6.2.0.exe", "test.txt")
    app.download()
