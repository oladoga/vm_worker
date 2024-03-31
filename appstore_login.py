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



def login_router_check():
    # 登录检查点，便利pics/login里面的图片会出现哪一个
    appstore_login_check=AppleStoreCheck()
    login_result = appstore_login_check.check_login()
    # 登录路由
    if login_result == "id_locked":
        logger.info("ID被锁定，返回结果，生命周期恢复。")
        return False,"id被锁定"
        pass
    elif login_result == "id_ok_mailcode":
        return True,"接受邮件验证码"
        pass
    elif login_result == "id_pwd_invalid":
        return False,"账号或者密码不正确"
        pass
    elif login_result == "id_ok_phone_num":
        return True,"接受手机验证码"
        pass
    elif login_result == "id_stoped":
        return False,"账号已经被停用"
        pass
    else:
        return False,"未适配错误！"



def do_task(apple_id,apple_id_pwd,email_api):

    # 默认设置为成功，遇到问题后会操作为失败
    result = True
    reason = ""

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

    #检测登录结果
    time.sleep(4)
    login_result,login_reson = login_router_check()


    if login_result:
        # 接收邮件验证码
        code = get_email_code(email_api)
        logger.info(code)
        time.sleep(5)
        login_result,login_reson = login_router_check()
    else:
        result=False

    if login_result:
        # 获取手机验证码
        phone_num,phone_url = get_mobile(host_url)
    else:
        phone_num,phone_url=("","")
        result=False

    return apple_id,apple_id_pwd,phone_num,phone_url,result,login_reson
