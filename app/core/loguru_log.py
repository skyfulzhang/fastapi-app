def get_logger(fp):
	from loguru import logger
	from pathlib import Path
	import time
	time_now = time.strftime("%Y-%m-%d", time.localtime(time.time()))
	log_format = "{time:YYYY-MM-DD at HH:mm:ss} | level:{level} | process:{process} | file:{file} | module:{name} | line:{line} | {message}"
	dir_path = Path.cwd().joinpath(fp)
	log_path = dir_path.joinpath(f"log_{time_now}.log")
	logger.add(log_path, format=log_format, retention='10 days', backtrace=True, diagnose=True, enqueue=True)
	return logger


logger = get_logger("logs")

"""
也可以使用 traceback 追溯异常信息
from loguru import logger
import traceback
def func():
    try:
       a=1 / 0
    except Exception as e:
       logger.info(traceback.format_exc())

"""
