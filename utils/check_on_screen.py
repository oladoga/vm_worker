import os
import cv2
import numpy as np
import pyautogui

def check_images_on_screen(path):
    result = {}

    # 获取指定路径下的所有文件
    files = os.listdir(path)

    # 遍历每个文件
    for file in files:
        # 检查文件是否为图片
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_path = os.path.join(path, file)
            template = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

            # 获取屏幕截图并转换为灰度图
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

            # 将模板也转换为灰度图
            if len(template.shape) > 2:
                template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            else:
                template_gray = template

            # 在截图中查找模板
            res = cv2.matchTemplate(screenshot, template_gray, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8 # 设定阈值
            loc = np.where(res >= threshold)

            if loc[0].size > 0:
                result[file] = True
            else:
                result[file] = False

    print(result)
    return result

# # 指定图片文件夹路径
# image_folder = "/Users/a/Desktop/ola_control/pics/login"

# # 检查图片是否出现在屏幕上
# image_results = check_images_on_screen(image_folder)
