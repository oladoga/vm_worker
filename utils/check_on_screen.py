import os
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
            screenshot = pyautogui.screenshot()

            # 检查截图中是否出现了图片
            if pyautogui.locateOnScreen(file_path) is not None:
                result[file] = True
            else:
                result[file] = False

    return result

# 指定图片文件夹路径
image_folder = "/Users/liangdong/PycharmProjects/macnode/pic"

# 检查图片是否出现在屏幕上
image_results = check_images_on_screen(image_folder)

print(image_results)
# 打印结果
for image, appeared in image_results.items():
    if appeared:
        print(f"图片 {image} 在屏幕上出现")
    else:
        print(f"图片 {image} 未在屏幕上出现")