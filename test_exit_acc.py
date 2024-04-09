from tasks.application import AppleStore
from loguru import logger
ret = AppleStore.click_logout()
logger.info(f"ret exit {ret.returncode}")
if ret == 1:
    logger.success("reg ok!!")
    result = True
    login_reason = "成功"
else:
    result = 0