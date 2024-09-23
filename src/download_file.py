import os
from log import Log; log = Log()
import requests, time
from alive_progress import alive_bar

"""
下载文件
输入值
url「下载链接」
path 「下载目录」
返回值
True 「下载成功」
False 「下载失败」
"""
def download(url: str, path: str) -> bool:
    if os.path.isfile(path):
        log.warning(f"文件「{path}」已存在")
        return True
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        if total_size == 0:
            log.error(f"下载「{path}」！原因：文件「{path}」大小为 0")
            return False
        block_size = 1024 * 10
        progress_bar_style = {
            "title": f"下载「{path}」",
            "bar": "blocks",
            "stats": ""
        }
        start_time = time.time()
        with alive_bar(total_size // block_size, enrich_print=False, manual=True, **progress_bar_style) as bar:
            with open(path, 'wb') as file:
                downloaded = 0
                for data in response.iter_content(block_size):
                    file.write(data)
                    downloaded += len(data)
                    bar(downloaded / total_size)
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 0:
                        speed = (downloaded / (1024 * 1024)) / elapsed_time
                        bar.text(f'速度: {speed:.2f} MB/s')
        return True
    except requests.exceptions.RequestException as e:
        log.error(f"下载「{path}」失败！原因：「{e}」")
    except Exception as e:
        log.error(f"下载「{path}」失败！原因：「{e}」")
    return False

if __name__ == "__main__":
    app = download("https://cdn.aliyundrive.net/downloads/apps/desktop/aDrive-6.2.0.exe", "../test_no_update/app.exe")
    print(f"Download Mod returned:{app}")
