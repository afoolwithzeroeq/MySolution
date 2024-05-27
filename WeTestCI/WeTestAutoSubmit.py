from WeTestAPI import *
import os

from WeTestAPI import default_gcloud, default_ios_gcloud

def get_tested_devices(restart : bool, save_file : str):
    if restart == True:
        cancel_all_test(save_file)
        return []
    tested_devices = []

    test_ids = []

    with open(save_file, "r") as f:
        for line in f.readlines():
            test_ids.append(int(line.strip()))

    print("已提交测试: ")
    print(test_ids)
    for test_id in test_ids:
        status, result, reason = get_test_results(test_id)
        if status != 200:
            print(status, result, reason)
            raise Exception("获取测试结果失败")
        else:
            for device in result["devices"]:
                tested_devices.append(device["device_id"])
    return tested_devices

def cancel_all_test(save_file : str):
    test_ids = []
    with open(save_file, "r") as f:
        for line in f.readlines():
            test_ids.append(int(line.strip()))
    for test_id in test_ids:
        status, result, reason = cancel_test(test_id)
        if status != 200:
            print(status, result, reason)
            print("取消测试失败: " + str(test_id))
        else:
            print("取消测试成功: " + str(test_id))
    with open(save_file, "w") as f:
        f.write("")

def submit_one_test(app_id : str, script_id : int, device_count : int, restart : bool, save_file : str, scriptInfo : str, platform : str, max_device_runtime : int, custom_device_ids : list = None):
    if restart == True:
        if os.path.exists(save_file):
            os.remove(save_file)
    
    if not os.path.exists(save_file):
        with open(save_file, "w") as f:
            f.write("")

    #读取最后一次测试ID
    last_test_id = 0
    test_ids = []
    with open(save_file, "r") as f:
        for line in f.readlines():
            if line.strip() == "test_success":
                print("测试已完成")
                return
            last_test_id = int(line.strip())
            test_ids.append(last_test_id)
    
    #查询最后一次测试状态
    count = 0
    if last_test_id != 0:
        status, result, reason = get_test_status(last_test_id)
        if status != 200:
            print(status, result, reason)
            raise Exception("获取测试状态失败")
        else:
            if result["test_status"]["finished"] != True:
                # print("上次测试未结束, 请等待测试结束后再提交新的测试")
                # return
                #获取未开始测试的设备
                status, result, reason = get_test_results(last_test_id)
                if status != 200:
                    print(status, result, reason)
                    raise Exception("获取测试详情失败")
                else:
                    for device in result["devices"]:
                        if device["result"] == "testing":
                            count += 1
                    
                    if count >= parallel_count:
                        leftFile = "left.txt"
                        lastCount = -1
                        if os.path.exists(leftFile):
                            with open(leftFile, 'r') as lastF:
                                lastCount = int(lastF.read())
                        if lastCount != count:
                            with open(leftFile, 'w') as lastF:
                                lastF.write(str(count))
                            send_wechat_message("当前测试进度: " + str(device_count - count) + '/' + str(device_count))
                        print("还有" + str(count) + "台设备未开始测试, 等待测试结束后再提交新的测试")
                        return
                    print("上次测试未结束, 但只有" + str(count) + "台设备测试中, 可以提交新的测试")

    if platform == "Android":
        gcloud_id = default_gcloud
    elif platform == "iOS":
        gcloud_id = default_ios_gcloud

    status, result, reason = get_devices(gcloud_id)
    if status != 200:
        print(status, result, reason)
        raise Exception("获取设备列表失败")
    all_devices = result["devices"]
    all_tested_devices = get_tested_devices(restart, save_file)
    print("已测试设备数量: " + str(len(all_tested_devices)))
    if custom_device_ids != None:
        print("自定义设备数量: " + str(len(custom_device_ids)))
    else:
        print("总设备数量: " + str(len(all_devices)))
    devices_to_test = []
    for device in all_devices:
        device_id = device["device_id"]
        if device["device_state"] == "available" and all_tested_devices.count(device_id) == 0:
            if custom_device_ids != None and custom_device_ids.count(device_id) == 0:
                continue
            devices_to_test.append(device_id)
            if len(devices_to_test) == device_count:
                break

    status, app_info, reason = get_app(app_id)
    if status != 200:
        print(status, app_info, reason)
        raise Exception("获取App信息失败")

    if len(devices_to_test) < 5:
        print("可用设备" + str(len(devices_to_test)) + "台")
        if count > 0:
            leftFile = "left.txt"
            lastCount = -1
            if os.path.exists(leftFile):
                with open(leftFile, 'r') as lastF:
                    lastCount = int(lastF.read())
            if lastCount != count:
                with open(leftFile, 'w') as lastF:
                    lastF.write(str(count))
                send_wechat_message("当前测试进度: " + str(device_count - count) + '/' + str(device_count))
            print("还有" + str(count) + "台设备测试中")
            return
        with open(save_file, "a") as f:
            f.write("test_success\n")
        sucess_message = "## Wetest自动提测\n"
        sucess_message += "测试信息:    " + scriptInfo + "\n"
        sucess_message += "测试平台:    " + platform + "\n"
        sucess_message += "AppName:     " + app_info["data"]["name"] + "\n"
        sucess_message += "AppVersion:  " + app_info["data"]["version"] + "\n"
        sucess_message += "AppID:       " + app_id + "\n"
        sucess_message += "ScriptID:    " + str(script_id) + "\n"
        sucess_message += "测试结果:    <font color=\"info\">测试完成</font>\n"
        fileName = str(app_id) + '_' + str(script_id) + '.xlsx'
        get_tests_details(test_ids, file_name=fileName)
        url = str(app_id) + "_" + str(script_id) + ".xlsx"
        sucess_message += "测试报告:    [" + url + "](" + url + ")\n"
        send_wechat_message(sucess_message, 'markdown')
        return
    print("提测设备数量: " + str(len(devices_to_test)))
    print(devices_to_test)
    status, result, reason = submit_test(app_id, script_id, len(devices_to_test), devices_to_test, cloud_id=gcloud_id, max_device_runtime=max_device_runtime)
    
    message = "## Wetest自动提测\n"
    message += "测试信息:    " + scriptInfo + "\n"
    message += "测试平台:    " + platform + "\n"
    message += "AppName:     " + app_info["data"]["name"] + "\n"
    message += "AppVersion:  " + app_info["data"]["version"] + "\n"
    message += "AppID:       " + app_id + "\n"
    message += "ScriptID:    " + str(script_id) + "\n"
    message += "本次提测数量: " + str(len(devices_to_test)) + "\n"
    
    if status != 200:
        print(status, result, reason)
        # raise Exception("提交测试失败")
        message += "测试结果:    <font color=\"warning\">提测失败</font>\n"
        message += "失败原因:    " + reason + "\n"
        send_wechat_message(message, "markdown")
        return
    
    test_id = result["test_info"]["test_id"]
    #追加写入文件
    with open(save_file, "a") as f:
        f.write(str(test_id) + "\n")
    print("提交测试成功, 测试ID: " + str(test_id))

    if custom_device_ids != None:
        message += "已提测数量:   " + str(len(all_tested_devices)) + " / " + str(len(custom_device_ids)) + "\n"
    else:
        message += "已提测数量:   " + str(len(all_tested_devices)) + " / " + str(len(all_devices)) + "\n"
    message += "# 测试报告: \n" + " >[https://console.wetest.net/app/testlab/automation/report/" + str(test_id) + "/](https://console.wetest.net/app/testlab/automation/report/" + str(test_id) + "/) \n"
    send_wechat_message(message, "markdown")

def send_wechat_message(content : str, msg_type : str = "text", web_key = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"):
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + web_key
    data = {"msgtype": msg_type, msg_type: {"content": content}}
    r = requests.post(url=webhook_url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    return r.text, r.status_code

def get_custom_devices(file : str = "custom_device.txt"):
    custom_device_ids = []
    if os.path.exists(file):
        with open(file, "r") as f:
            for line in f.readlines():
                custom_device_ids.append(int(line.strip()))
    return custom_device_ids

import base64
import hashlib
import json
import requests

def send_image_to_wechat(dir_path, wx_id):
    with open(dir_path, 'rb') as file:
        file_content = file.read()

    base64_content = base64.b64encode(file_content).decode()
    md5_hash = hashlib.md5(file_content).hexdigest()

    payload = {
        "msgtype": "image",
        "image": {
            "base64": base64_content,
            "md5": md5_hash
        }
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={wx_id}",
        headers=headers,
        json=payload
    )

    return response.text, response.status_code

def send_news_to_wechat(title, description, url, picurl, wx_id):
    payload = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": title,
                    "description": description,
                    "url": url,
                    "picurl": picurl
                }
            ]
        }
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={wx_id}",
        headers=headers,
        json=payload
    )

    return response.text, response.status_code

import sys
if __name__ == '__main__':
    if len(sys.argv) < 7:
        raise Exception("参数不足")
    app_id = sys.argv[1]
    script_id = int(sys.argv[2])
    save_file = app_id + "_" + str(script_id) + ".txt"
    device_count = int(sys.argv[3])
    restart = sys.argv[4] == "true"
    useCustomIds = sys.argv[5] == "true"
    scriptInfo = sys.argv[6]
    platform = sys.argv[7]
    max_device_runtime = int(sys.argv[8])
    print(scriptInfo)
    if useCustomIds:
        custom_device_ids = get_custom_devices()
        submit_one_test(app_id, script_id, device_count, restart, save_file, scriptInfo, platform, max_device_runtime, custom_device_ids)
    else:
        submit_one_test(app_id, script_id, device_count, restart, save_file, scriptInfo, platform, max_device_runtime)
