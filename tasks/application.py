import subprocess
from loguru import logger
import time
import os
import pyautogui
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.check_on_screen import check_images_on_screen
class AppleStore():
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def kill_app(time_sleep=5):
        # 定义要执行的AppleScript命令
        logger.info("杀死apple store")
        applescript_code = '''
        tell application "System Events"
            set appProcess to first process whose name is "App Store"
            if exists appProcess then
                do shell script "kill -9 " & (unix id of appProcess)
            end if
        end tell
        '''
        # 执行AppleScript命令
        subprocess.run(['osascript', '-e', applescript_code])
        time.sleep(time_sleep)


    @staticmethod
    def open_app(time_sleep=5):
        # 定义要执行的AppleScript命令
        logger.info("打开apple store")
        applescript_code = '''
        tell application "App Store"
            activate
        end tell
        '''
        # 执行AppleScript命令
        subprocess.run(['osascript', '-e', applescript_code])
        time.sleep(time_sleep)

    @staticmethod
    def click_login():
        app_code ='''
        tell application "System Events"
            tell process "App Store"
                -- 点击菜单栏中的"商店"
                click menu bar item "商店" of menu bar 1
                
                -- 等待菜单显示
                delay 2
                
                -- 点击下拉菜单中的"登录"
                click menu item "登录" of menu 1 of menu bar item "商店" of menu bar 1
            end tell
        end tell
        '''
        # 执行AppleScript命令
        subprocess.run(['osascript', '-e', app_code])
        pass

    @staticmethod
    def input_apple_id(apple_id):
        logger.info(f"输入苹果ID——{apple_id}")
        # 输入文本
        pyautogui.typewrite(apple_id)
        # 模拟按下回车键
        pyautogui.press("enter")
        pass

    @staticmethod
    def input_apple_id_pwd(apple_id_pwd):
        logger.info(f"输入苹果ID密码——{apple_id_pwd}")
        # 输入文本
        pyautogui.typewrite(apple_id_pwd)
        # 模拟按下回车键
        pyautogui.press("enter")
        pass


class AppleStoreCheck(object):
    def __init__(self) -> None:
        self.pics_path = "pics/login"
        pass

    def check_login(self):
        ret = check_images_on_screen(self.pics_path)
        for _ret in ret.keys():
            if ret[_ret] is True:
                logger.info(_ret)
                return _ret.replace(".png","")
            else:
                logger.info(f"not find {_ret}")

        pass

# aps_check = AppleStoreCheck()
# aps_check.check_login()