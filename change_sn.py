import base64
import plistlib
import struct

config_path = "/Volumes/OPENCORE/EFI/OC/config.plist"

import plistlib


def update_config_with_five_code(plist_file, sn, board_id, model_id, sys_uuid, mlb, rom):
    # 读取plist文件
    with open(plist_file, 'rb') as file:
        plist_data = plistlib.load(file)

    rom = bytes.fromhex(rom)
    # Generic
    plist_data['PlatformInfo']['Generic']['SystemSerialNumber'] = sn
    plist_data['PlatformInfo']['Generic']['SystemProductName'] = model_id
    plist_data['PlatformInfo']['Generic']['MLB'] = mlb
    plist_data['PlatformInfo']['Generic']['SystemUUID'] = sys_uuid
    plist_data['PlatformInfo']['Generic']['ROM'] = rom

    # PlatformNVRAM
    plist_data['PlatformInfo']['PlatformNVRAM']['SystemSerialNumber'] = sn
    plist_data['PlatformInfo']['PlatformNVRAM']['BID'] = board_id
    plist_data['PlatformInfo']['PlatformNVRAM']['MLB'] = mlb
    plist_data['PlatformInfo']['PlatformNVRAM']['SystemUUID'] = sys_uuid
    plist_data['PlatformInfo']['PlatformNVRAM']['ROM'] = rom

    # DataHUB
    plist_data['PlatformInfo']['DataHub']['SystemSerialNumber'] = sn
    plist_data['PlatformInfo']['DataHub']['SystemProductName'] = model_id
    plist_data['PlatformInfo']['DataHub']['BoardProduct'] = board_id
    plist_data['PlatformInfo']['DataHub']['SystemUUID'] = sys_uuid

    # DataHUB
    plist_data['PlatformInfo']['SMBIOS']['ChassisSerialNumber'] = sn
    plist_data['PlatformInfo']['SMBIOS']['SystemSerialNumber'] = sn
    plist_data['PlatformInfo']['SMBIOS']['SystemProductName'] = model_id
    plist_data['PlatformInfo']['SMBIOS']['ChassisVersion'] = board_id
    plist_data['PlatformInfo']['SMBIOS']['SystemUUID'] = sys_uuid

    plist_data['PlatformInfo']['SMBIOS']['BoardProduct'] = board_id
    plist_data['PlatformInfo']['SMBIOS']['BoardSerialNumber'] = mlb
    plist_data['PlatformInfo']['SMBIOS']['BoardVersion'] = model_id

    plist_data['PlatformInfo']['SMBIOS']['Family'] = "MacBook Air"

    # system



    # 写入更新后的内容到plist文件
    with open(plist_file, 'wb') as file:
        plistlib.dump(plist_data, file)

    print(f"已成功更新配置文件：{plist_file}")


# 示例用法
plist_file_path = '/Volumes/OPENCORE/EFI/OC/config_1.plist'
_sn = 'ABCDE12345'  # 替换为你的五码值
_board_id = 'BOARD-ID'
_model_id = 'MODEL,1'
_sys_uuid = 'DSADSADSA-DSADASDSA-DSADSA'
_mlb = 'FV98166019MJ2V888'
_rom = '846878006880'

# update_config_with_five_code(plist_file_path, _sn, _board_id, _model_id, _sys_uuid, _mlb, _rom)
