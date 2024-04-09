from tasks.application import AppleStore
from tasks.application import AppleStoreCheck
from loguru import logger
import time
from apis.code_api import get_email_code, get_mobile_code, get_hotmail_code_pop3, get_selfbuild_code_pop3
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


# do functions


def do_task(apple_id, apple_id_pwd, email_api):
    # 默认设置为成功，遇到问题后会操作为失败
    global phone_num, phone_url
    result = False
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

    # status router
    step_count = 4
    step_max_time = 40
    step_once_time = 5
    loop_time = int(step_max_time / step_once_time)
    step_record = None
    login_reason = ""
    for i in range(step_count):
        success = False  # 标记是否成功获取验证码
        fatal_error = False
        for z in range(loop_time):
            appstore_login_check = AppleStoreCheck()
            login_result = appstore_login_check.check_login()
            # 登录路由
            if login_result == "id_locked":
                logger.info("ID被锁定，返回结果，生命周期恢复。")
                login_reason = "ID被锁定"
                fatal_error = True
                break
            elif login_result == "id_ok_mailcode":
                max_attempts = 3
                attempts = 0
                code = ""
                while attempts < max_attempts and not code:
                    if "http" in email_api:
                        code = get_email_code(email_api)
                    elif "hotmail" in apple_id:
                        code = get_hotmail_code_pop3(apple_id, email_api)
                    else:
                        code = get_selfbuild_code_pop3(apple_id, email_api)
                    attempts += 1
                    time.sleep(2)
                if code:
                    print("成功获取到验证码:", code)
                    AppleStore.input_apple_id_maillcode(code)
                    login_reason = '成功获取到验证码'
                else:
                    print("无法获取验证码")
                    login_reason = '无法获取验证码'

            elif login_result == "id_pwd_invalid":
                login_reason = '账号或者密码不正确'
                fatal_error = True
                break
            elif login_result == "id_ok_phone_num":
                phone_num, phone_url = get_mobile(host_url)
                AppleStore.input_apple_id_input_mobile(phone_num)
                sms_code = get_mobile_code(phone_url)
                AppleStore.input_apple_id_maillcode(sms_code)
                time.sleep(28)

                ret = AppleStore.click_logout()
                logger.info(f"ret exit {ret.returncode}")
                if ret.returncode == 0:
                    logger.success("reg ok!!")
                    result = True
                    login_reason = "成功"
                    break
                else:
                    result = 0
                    login_reason = "退出失败"
            elif login_result == "id_stoped":
                login_reason = "账号已经被停用"
                fatal_error = True
                break
            elif login_result == "id_error_mailcode_invalid":
                login_reason = "邮件验证码错误"
                break
            else:
                logger.info("waiting")
            time.sleep(1)
        if success:
            break
        if fatal_error:
            break
        if login_reason != "成功":
            result = False

    return apple_id, apple_id_pwd, phone_num, phone_url, result, login_reason
