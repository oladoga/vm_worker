from tasks.application import AppleStore
from tasks.application import AppleStoreCheck
from loguru import logger
import time
from apis.code_api import get_email_code,get_mobile_code
import requests

host_url = 'http://192.168.0.111:8000'  # 主机管理服务器的地址

def get_mobile(host_url):
    logger.info("申请获取接码API")
    ret = requests.get(f'{host_url}/get_mobile')
    logger.info(ret.json())
    return ret.json()['mobile'],ret.json()['url']

def do_task(apple_id,apple_id_pwd,email_api):
    # 准备工作，杀死AppStore
    AppleStore.kill_app()
    
    # 第一步，先打开app store，检查点为
    AppleStore.open_app()
    
    # 第二步，点击登录按钮
    AppleStore.click_login()
    
    # 第三步，输入AppleID
    time.sleep(6)
    AppleStore.input_apple_id(apple_id)

    time.sleep(3)
    AppleStore.input_apple_id_pwd(apple_id_pwd)

    # 登录检查点
    login_result = AppleStoreCheck.check_login()

    # 登录路由
    if login_result == 0x01:
        pass

    # 接收邮件验证码

    code = get_email_code(email_api)
    logger.info(code)

    # 获取手机验证码
    phone_num,phone_url = get_mobile(host_url)
    result = True

    return apple_id,apple_id_pwd,phone_num,phone_url,result
