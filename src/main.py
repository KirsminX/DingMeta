from datetime import timezone
import asyncio
from log import Log
from parse_config import Config
"""
DingMeta 源码
作者    Kirsmin/KirsminX
协议    MIT License
版本    Alpha
"""

def main():
    config = Config()
    console_config = config.getter("Console")
    if console_config["Log"]["log_mode"] == "file":
        written = True
    else:
        written = False
    log = Log(debug=console_config["Log"]["debug"], written=written, memorize=True, timezone=console_config["time_zone"])
    log.info("Hello")

if __name__ == "__main__":
    main()