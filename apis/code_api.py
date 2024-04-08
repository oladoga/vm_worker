import time
import requests
from loguru import logger
import re
import poplib
from email import parser
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




def fetch_latest_email(username, password, server):
    # 连接到 POP3 服务器
    pop_conn = poplib.POP3(server,port=110)

    # 发送身份验证信息
    pop_conn.user(username)
    pop_conn.pass_(password)

    # 获取邮件总数和邮件列表
    num_emails = len(pop_conn.list()[1])
    # 获取最新一封邮件的索引
    latest_email_index = num_emails

    # 获取最新一封邮件
    response, lines, octets = pop_conn.retr(latest_email_index)
    # 将邮件内容合并为字符串
    email_content = b'\n'.join(lines).decode('utf-8')

    # 解析邮件内容
    email_parser = parser.Parser()
    email = email_parser.parsestr(email_content)

    # 关闭连接
    pop_conn.quit()
    for i in email.get_payload():
        if i.get_content_type() == 'text/plain':
            return i.get_payload()
    # 返回最新一封邮件的内容
    return email.get_payload()

def get_hotmail_code_pop3(email,password):
    # 获取输入的邮箱和密码
  
    server = '119.28.102.159'

    try:
        latest_email_content = fetch_latest_email(email, password, server)
        email_content = latest_email_content
        pattern = r'(\d{6})'  # 匹配6位数字
        match = re.search(pattern, email_content)
        if match:
            verification_code = match.group(1)
            logger.success(f"验证码获取成功：「{verification_code}」")
            return verification_code
        else:
            logger.error("验证码没有获取到.")
    except Exception as e:
        logger.error(f"viryfcation code fetch error:{e}")
# ret = get_hotmail_code_pop3("VerleneNave172@outlook.com","FBKJXcNgUn62")
# print(ret)