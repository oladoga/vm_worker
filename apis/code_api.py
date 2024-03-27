import time
import requests
from loguru import logger
import re


def get_mobile_code(mobile_api_url, refresh=4, interval=10,delay_before=5):
    time.sleep(delay_before)
    try:
        count = 0
        while count < refresh:
            res = requests.get(mobile_api_url).text
            if "message" in res:
                logger.error(f"第{count+1}次尝试，暂未收到验证码")
            else:
                pattern = r"\b\d{6}\b"
                matches = re.findall(pattern, res)
                if matches:
                    code = matches[0]
                    logger.info(f"匹配到的手机验证代码为：{code}")
                    return code
                else:
                    print("未找到符合要求的代码。")

            count += 1
            if count < refresh:
                time.sleep(interval)

    except Exception as e:
        logger.error(e)


def get_email_code(email_api_url, refresh=4, interval=10, delay_before=5):
    time.sleep(delay_before)
    try:
        count = 0
        while count < refresh:
            res = requests.get(email_api_url)
            if res.status_code == 200:
                text = res.content.decode()
                logger.info(text)
                match = re.search(r'<b>(\d+)</b>', text)
                if match:
                    verification_code = match.group(1)
                    return verification_code
                else:
                    match = re.search(r'<p>(\d+)</p>', text)
                    if match:
                        verification_code = match.group(1)
                        return verification_code
                    else:
                        logger.error(f"第{count+1}次解析失败，接码平台格式错误或未收到邮件验证码,。")
            else:
                logger.error(res)
                logger.error("请求失败，请检查URL是否正确")

            count += 1
            if count < refresh:
                time.sleep(interval)

    except Exception as e:
        logger.error("发生异常，请检查网络连接或URL是否正确")
pass