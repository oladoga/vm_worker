import json
import time
import uuid

from loguru import logger
import requests
import platform
import subprocess
import socket
import re
from appstore_login import do_task
from change_sn import update_config_with_five_code

host_url = 'http://oladoga.x3322.net:1988'  # 主机管理服务器的地址


def get_lifecycle(host_url):
    logger.info("获取生命周期设置")
    ret = requests.get(f'{host_url}/lifecycle_get')
    logger.debug(ret.json())
    return ret.json()['lifecycle']


def get_host_ip():
    ip = socket.gethostbyname(socket.gethostname())
    ip_part = ip.split('.')
    _ip_part = [ip_part[0], ip_part[1], ip_part[2], "1"]
    host_ip = '.'.join(_ip_part)
    return f"http://{host_ip}"


def get_mac_serial_number():
    system = platform.system()
    if system == "Darwin":
        command = "system_profiler SPHardwareDataType | awk '/Serial Number/ {print $4}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout.strip()
        logger.info(f"获取本机器SN成功{output}")
        return output
    else:
        return None

def get_mac_addr():
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                            for ele in range(0, 8 * 6, 8)][::-1])
    logger.info(f"get the mac is {mac_address}")
    return mac_address



def change_sn_by_oc():
    five_code = requests.get(f'{host_url}/get_sn').json()
    logger.info(five_code)
    def generate_uuid():
        # 生成带有短划线的 UUID
        generated_uuid = uuid.uuid4()
        # 返回字符串形式的 UUID
        return str(generated_uuid).upper()
    _sn = five_code['sn']
    _rom = five_code["rom"]
    _board_id = five_code['board_id']
    _model_id = five_code['hw_model']
    _mlb = five_code['mlb']
    _sys_uuid = generate_uuid()
    plist_file_path = '/Volumes/OPENCORE/EFI/OC/config.plist'
    update_config_with_five_code(plist_file_path, _sn, _board_id, _model_id, _sys_uuid, _mlb, _rom)
    pass

def register_with_host(host_url, sn, status, lifecycle):
    # logger.info(f"向主控注册信息sn:{sn},状态{status},生命周期：{lifecycle}")
    _response = requests.post(f'{host_url}/reg', data=json.dumps({'sn': sn, 'status': status, 'lifecycle': lifecycle}))
    if _response.status_code == 200:
        logger.info(f"成功向主控注册信息sn:{sn},状态{status},生命周期：{lifecycle}")

def get_mobile(host_url):
    logger.info("申请获取接码API")
    ret = requests.get(f'{host_url}/get_mobile')
    logger.info(ret.json())


def query_change_sn():
    logger.info("该SN生命周期已完成，请求更换SN")
    try:
        requests.post(f'{get_host_ip()}:8001/change_sn', json.dumps({"mac": get_mac_addr()}))
    except Exception as e:
        logger.error(e)
        pass
    requests.post(f'{host_url}/reg_del', json.dumps({"sn": sn}))


def task_accept():
    logger.info("任务接受，通知主控改变改任务状态。")
    ret = requests.get(f'{host_url}/task_accept/{sn}/')


def execute_task(_task):

    logger.info(f"开始执行任务{_task}")
    global lifecycle
    lifecycle -= 1
    register_with_host(host_url, sn, status="busy", lifecycle=lifecycle)
    task_accept()
    task_result = do_task(task["apple_id"], task['password'], task['mail_url'])

    # 执行任务的逻辑
    # 最后一次任务执行完毕后，不在更新为free，直接申请换sn

    # 重新注册信息为free
    register_with_host(host_url, sn, status="free", lifecycle=lifecycle)
    return task_result


def submit_result(ret):
    """
    apple_id: str
    password: str
    mobile: str
    mobile_url: str
    result: int
    """
    appleid, pwd, phone, phoneurl, result, reason = ret
    logger.info("任务完成，回馈结果。")
    _result = {"apple_id": appleid, "password": pwd, "mobile": phone, "mobile_url": phoneurl, "result": result,
               "reason": reason}

    _response = requests.post(f'{host_url}/task_done', data=json.dumps(_result))
    if _response.status_code == 200:
        logger.info(f"回馈结果成功")


if __name__ == '__main__':
    try:
        sn = get_mac_serial_number()  # 虚拟机ID
        if sn == "FVFW102SJ1WK":
            logger.info("need change sn")
            change_sn_by_oc()
            exit(9)
        lifecycle = get_lifecycle(host_url)
        register_with_host(host_url, sn, status="free", lifecycle=lifecycle)
        while True:
            try:
                response = requests.get(f'{host_url}/task_get')
                task = response.json().get(sn)
                if task is not None:
                    ret = execute_task(task)
                    submit_result(ret)
                    if lifecycle == 0:
                        query_change_sn()
                        exit()
                else:
                    logger.info("等待主控发配任务")
                    if lifecycle == 0:
                        register_with_host(host_url, sn, status="busy", lifecycle=lifecycle)
                    else:
                        register_with_host(host_url, sn, status="free", lifecycle=lifecycle)

                time.sleep(2)
            except Exception as e:
                logger.error(f"严重错误「{e}」")
                if lifecycle == 0:
                    query_change_sn()
                    exit()
            # tasks = response.json()['tasks']
            # for task in tasks:
            #     execute_task(task)
            # # 完成任务后，向主机管理服务器报告
            # requests.post(f'{host_url}/tasks', json={'vm_id': vm_id, 'completed_tasks': tasks})
    except Exception as e:
        logger.error(f"严重错误「{e}」")
