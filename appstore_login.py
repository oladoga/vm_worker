from tasks.application import AppleStore
from tasks.application import AppleStoreCheck
from loguru import logger
import time
from apis.code_api import get_email_code, get_mobile_code, get_hotmail_code_pop3
import requests

host_url = 'http://oladoga.x3322.net:1988'  # 主机管理服务器的地址


def get_mobile(host_url):
    logger.info("申请获取接码API")
    ret = requests.get(f'{host_url}/get_mobile')
    logger.info(ret.json())
    return ret.json()['mobile'], ret.json()['url']


def login_router_check():
    # 登录检查点，便利pics/login里面的图片会出现哪一个
    appstore_login_check = AppleStoreCheck()
    login_result = appstore_login_check.check_login()
    # 登录路由
    if login_result == "id_locked":
        logger.info("ID被锁定，返回结果，生命周期恢复。")
        return False, "id被锁定"
        pass
    elif login_result == "id_ok_mailcode":
        return True, "接受邮件验证码"
        pass
    elif login_result == "id_pwd_invalid":
        return False, "账号或者密码不正确"
        pass
    elif login_result == "id_ok_phone_num":
        return True, "接受手机验证码"
        pass
    elif login_result == "id_stoped":
        return False, "账号已经被停用"
        pass
    elif login_result == "id_error_mailcode_invalid":
        return False, "邮件验证码错误"
        pass
    else:
        return False, "未适配错误！"


def do_task(apple_id, apple_id_pwd, email_api):
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

    # 检测登录结果
    time.sleep(20)
    login_result, login_reson = login_router_check()

    def get_email_code(email_api):
        _code = ""
        if "http" in email_api:
            _code = get_email_code(email_api)
        else:
            _code = get_hotmail_code_pop3(apple_id, email_api)
        AppleStore.input_apple_id_maillcode(_code)

    if login_result:
        # 接收邮件验证码
        for i in range(3):
            time.sleep(4)
            get_email_code(email_api)
            time.sleep(12)
            login_result, login_reson = login_router_check()
            if login_result:
                break
            if "邮件验证码错误" in login_reson:
                get_email_code(email_api)
                time.sleep(12)
                login_result, login_reson = login_router_check()
            else:
                break
    else:
        result = False

    if login_result:
        # 获取手机验证码
        phone_num, phone_url = get_mobile(host_url)
        AppleStore.input_apple_id_input_mobile(phone_num)
        sms_code = get_mobile_code(phone_url)
        AppleStore.input_apple_id_maillcode(sms_code)

    else:
        phone_num, phone_url = ("", "")
        result = False

    if login_result:
        time.sleep(10)
        logger.info("成功")
        ret = AppleStore.click_logout()
        if ret == 1:
            result = 1
            login_reson = "成功"
        else:
            result = 0
            login_reson = "退出失败"

    return apple_id, apple_id_pwd, phone_num, phone_url, result, login_reson
