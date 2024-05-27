import json
import requests

"""
automation api for wetest
see details on "https://www.wetest.net/documents/detail/automation/v4W7Vvyn"
"""

default_gcloud = 5
default_ios_gcloud = 3
project_id = "xxxxx" #项目ID
SecretId = "xxxxx" #SecretId
SecretKey = "xxxxx" #SecretKey
frame_type = "airtest1.2.6"

parallel_count = 5

def curl_get(url : str):
    """
    curl -u <SecretId>:<SecretKey> <url>
    """
    r = requests.get(url, auth=(SecretId, SecretKey))
    return r.status_code, r.json(), r.reason

def curl_post(url : str, json_data : str = None, file_path : str = None):
    """
    curl -u <SecretId>:<SecretKey> --request POST <url> -d <json_data> --form "data=@<file_path>"
    """
    if file_path is None:
        r = requests.post(url, auth=(SecretId, SecretKey), json=json_data)
    else:
        file = {'file': open(file_path, 'rb')}
        r = requests.post(url, auth=(SecretId, SecretKey), json=json_data, files=file)
    return r.status_code, r.json(), r.reason

def curl_delete(url : str):
    """
    curl -u <SecretId>:<SecretKey> --request DELETE <url>
    """
    r = requests.delete(url, auth=(SecretId, SecretKey))
    return r.status_code, r.json(), r.reason

def upload_app(app_name : str, app_path : str):
    """
    curl -u <SecretId>:<SecretKey> --request POST "https://api.paas.wetest.net/cloudtest/v1/platform/upload/storage?project=<project>&name=<app_name>" --form "data=@<app_path>"
    :param app_name: app name with extension(.aab, .apk, .ipa)
    :param app_path: absolute local path of your app file
    :return: {
        "data": {
            "fid": string,  // app hash id used for submit test 
        },
        "msg": "string",
        "ret": int
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/platform/upload/storage?project=" + project_id + "&name=" + app_name
    return curl_post(url, None, app_path)

def get_app(fid : str):
    """
    curl -u <SecretId>:<SecretKey> "https://api.paas.wetest.net/cloudtest/v1/platform/upload/info?fid=<fid>&project=<project>"
    :param fid: app hash id
    :return: {
        "msg": "string",
        "ret": int,
        "data": {
            "fid": "string",        // app hash id
            "size": int,            // app size (bytes)
            "md5": "string",        // app md5 hash
            "url": "string",        // app download url
            "name": "string",       // app name
            "package": "string",    // app package
            "version": "string",    // app version
            "icon_url": "string"    // icon download url
        }
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/platform/upload/info?fid=" + fid + "&project=" + project_id
    return curl_get(url)

def delete_app(fid : str):
    """
    curl -u <SecretId>:<SecretKey> --request DELETE "https://api.paas.wetest.net/cloudtest/v1/platform/upload/info/<fid>"
    :param fid: app hash id
    :return:{
        "msg": "string",
        "ret": int
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/platform/upload/info/" + fid
    return curl_delete(url)

def upload_script(file_path : str):
    """
    curl -u <SecretId>:<SecretKey> --request POST "https://api.paas.wetest.net/cloudtest/v1/scripts" --form "file=@<file_path>" 
    :param file_path: absolute local path of your script file
    :return:{
        "script": {
            "script_id": int,        // script id used for submit test 
            "size": int,             // script size (bytes)
            "script_url": "string",  // script download url
        },
        "msg": "string",
        "ret": int
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/scripts"
    return curl_post(url, None, file_path)

def get_script(script_id : int):
    """
    curl -u <SecretId>:<SecretKey> "https://api.paas.wetest.net/cloudtest/v1/scripts/<script_id>"
    :param script_id: script id
    :return:{
        "script": {
            "script_id": int,      // script id used for submit test 
            "user": "string",      // upload user id
            "size": int,           // script size (bytes) 
            "script_url": "string",// script download url
            "project": "string"    // script upload project
        },
        "msg": "string",
        "ret": int
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/scripts/" + str(script_id)
    return curl_get(url)

def delete_script(script_id : int):
    """
    curl -u <SecretId>:<SecretKey> --request DELETE "https://api.paas.wetest.net/cloudtest/v1/scripts/<script_id>"
    :param script_id: script id
    :return:{
        "msg": "string",
        "ret": int
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/scripts/" + str(script_id)
    return curl_delete(url)

def get_gcloud_list():
    """
    curl -u <SecretId>:<SecretKey> "https://api.paas.wetest.net/cloudtest/v1/users/clouds"
    :return:{
        "clouds": [{
            "cloud_id": int,
            "cloud_name": "string",
        }],
        "msg": "string",
        "ret": int // 0 for success
    } 
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/users/clouds"
    return curl_get(url)

def get_devices(gcloud_id : int = default_gcloud):
    """
    curl -u <SecretId>:<SecretKey> "https://api.paas.wetest.net/cloudtest/v1/clouds/<cloud_id>/devices"
    :param gcloud_id: gcloud id
    :return:{
        "devices": [{
            "cloud_id": int,             // Device Farm ID
            "cpu_total": int,            // device cpu core number
            "device_id": int,            // device ID
            "device_state": "string",    // device state
            "device_state_code": int,    // device state code
            "location": "string",        // device location
            "manufacture": "string",     // manufacture
            "model": "string",           // model name
            "model_id": int,             // model ID
            "ram": int,                  // ram
            "resolution": "string",      // resolution
            "test_id": int,              // current test ID
            "version": "string",         // system version
        }],
        "msg": "string",
        "ret": int
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/clouds/" + str(gcloud_id) + "/devices"
    return curl_get(url)

def get_custom_model_list():
    """
    curl -u <SecretId>:<SecretKey> "https://api.paas.wetest.net/cloudtest/v1/model/list?project=<project>"
    :return:{
        "count": int,             // list count
        "data": [{
            "id": int,              // list ID
            "name": "string",       // list name
            "cloud_name": "string", // device farm name
            "device_type": int,     // device type 0 for android 1 for ios
            "model_count": int,     // model or device count in this list 
            "cloud_id": int,        // device farm id
            "filter_type": int      // saved as device or model dimension. 1 for model list 2 for device list
        }], 
        "msg": "string",
        "ret": int
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/model/list?project=" + project_id
    return curl_get(url)

def submit_test(app_id : str, script_id : int, device_number : int, devices : list = None, device_choose_type : str = None, max_device_runtime : int = 1200, cloud_id : int = default_gcloud):
    """
    curl -u <SecretId>:<SecretKey> --request POST "https://api.paas.wetest.net/cloudtest/v1/tests/automation" 
    -d '{
        "app_hash_id": <app_id>,
        "cloud_id":<cloud_id>,
        "script_id": <script_id>,
        "frame_type":<frame_type>
        "max_test_runtime": 1800,
        "device_number": 2,
        "project": <project>
    }'
    :param app_id: Target App ID
    :param script_id: Target script ID
    :param device_number: Target device quantity
    :param devices: Choose device ID or model ID for submit test. Mix device ID and model ID are not allowed.
    :param device_choose_type: Target device strategy, device ID or model ID.
        “deviceids”: choose device group by device ID
        “modelids”: choose device group by model ID
        :default value is “deviceids”
    :param max_device_runtime: The time out period of the each device. The default is 600 seconds.
    :param max_test_runtime: The time out period of the entire test, The default is 1800 seconds.
    :param cloud_id: gcloud id
    :return:{
        "msg": "string",
        "ret": int,
        "test_info": {
            "test_id": int // test ID
        }
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/tests/automation"
    max_test_runtime = int(max_device_runtime * (device_number + parallel_count) / parallel_count) + 300
    data = {
        "app_hash_id": app_id,
        "cloud_id": cloud_id,
        "script_id": script_id,
        "frame_type": frame_type,
        "max_test_runtime": max_test_runtime,
        "max_device_runtime": max_device_runtime,
        "device_number": device_number,
        "project": project_id,
        "devices": devices,
        "device_choose_type": device_choose_type,
        "email_notify":False,
        "resign":True,
    }
    return curl_post(url, data)

def cancel_test(test_id : int):
    """
    curl -u <SecretId>:<SecretKey> --request POST "https://api.paas.wetest.net/cloudtest/v1/tests/<test_id>/cancelation"
    :param test_id: test id
    :return: {
        "msg": "string",
        "ret": int
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/tests/" + str(test_id) + "/cancelation"
    return curl_post(url)

def get_test_status(test_id : int):
    """
    curl -u <SecretId>:<SecretKey>  "https://api.paas.wetest.net/cloudtest/v1/tests/<test_id>/status"
    :param test_id: test id
    :return:{
        "msg": "string",
        "ret": int,
        "test_status": {
            "finished": bool,        // whether the task is finished
            "start_time": "string",  // test start time
            "end_time": "string",    // test end time
            "test_id": int,          // test ID
            "status_code": int,    // test status,0 for testing,1 for fnished, 2 for canceled,3 for test timeout
            "status":"string"      // test status description
        }
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/tests/" + str(test_id) + "/status"
    return curl_get(url)

def get_test_results(test_id : int, log : bool = False, image : bool = False, error : bool = False):
    """
    curl -u <SecretId>:<SecretKey>  "https://api.paas.wetest.net/cloudtest/v1/tests/<test_id>/devices?log=<log>&image=<image>&error=<error>"
    :param test_id: test id
    :param log: whether to return the log, default is false
    :param image: whether to return the screenshot, default is false
    :param error: whether to return the error information, default is false
    :return:{
        "devices": [{
            // test ID
            "test_id": int,
            // device ID
            "device_id": int,
            // submit time of device
            "start_time": "string",
            // start time of device
            "device_start_time": "string",
            // queuing time of device, the unit is seconds
            "wait_time": 0,
            // end time of device
            "end_time": "string",
            // if parameter error is set to true,return error details
            "errors": [{
            "content": "string",
            "description": "string",
            "error_time": "string",
            "level": "string"
            }], 
            // if parameter image is set to true,return image details
            "images": [{
            "image_name": "string",
            "image_time": "string",
            "image_url": "string"
            }],
            // if parameter log is set to true,return mobile log,script log and video
            "mobile_log_url": "string",
            "script_log_url": "string",
            "test_video_url": "string",
            // if test is functional test,reture tested case details on this device
            "case_stat": {
            "case_total": int,    // number of total case
            "case_success": int,  // number of successful case 
            "case_fail": int,     // number of failed case 
            "case_timeout": int   // number of timeout case 
            },
            // device detail information
            "model": "string",
            "version": "string",
            "manufacture":"string",
            "ram":int,
            "cpu_ghz":float,
            "cpu_total":int,
            // Description of device result. If it is a functional test, you don't need to pay much attention to this information. You should focus on case results.
            "result": "string",
            // device result code
            // 0 for running, 1 for passed, 2 for has compatibility error, 3 for untest（caused by device exception, 4 for timeout, 5 for system canceled, 6 for user canceled
            "result_code": 0,
            // device process cost
            "cost_info":[{
            "process_name":"string", // process name means what device is doing
            "cost":int,              // cost time, unit is seconds
            "start_time":"string",   // start time of this process
            "end_time":"string"      // end time of this process
            }],
        }],
        "msg": "string",
        "ret": int
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/tests/" + str(test_id) + "/devices?log=" + str(log) + "&image=" + str(image) + "&error=" + str(error)
    return curl_get(url)

def get_device_test_result(test_id : int, device_id : int, log : bool = False, image : bool = False, error : bool = False):
    """
    curl -u <SecretId>:<SecretKey>  "https://api.paas.wetest.net/cloudtest/v1/tests/<test_id>/devices/<device_id>?log=<log>&image=<image>&error=<error>"
    :param test_id: test id
    :param device_id: device id
    :param log: whether to return the log, default is false
    :param image: whether to return the screenshot, default is false
    :param error: whether to return the error information, default is false
    :return:{
        "device": {
            // test ID
            "test_id": int,
            // device ID
            "device_id": int,
            // submit time of device
            "start_time": "string",
            // start time of device
            "device_start_time": "string",
            // queuing time of device, the unit is seconds
            "wait_time": 0,
            // end time of device
            "end_time": "string",
            // if parameter error is set to true,return error details
            "errors": [{
            "content": "string",
            "description": "string",
            "error_time": "string",
            "level": "string"
            }],
            // if parameter image is set to true,return image details
            "images": [{
            "image_name": "string",
            "image_time": "string",
            "image_url": "string"
            }],
            // if parameter log is set to true,return mobile log,script log and video
            "mobile_log_url": "string",
            "script_log_url": "string",
            "test_video_url": "string",
            // if test is functional test,reture tested case details on this device
            "case_stat": {
            "case_total": int,    // number of total case
            "case_success": int,  // number of successful case 
            "case_fail": int,     // number of failed case 
            "case_timeout": int   // number of timeout case 
            },
            // device detail information
            "model": "string",
            "version": "string",
            "manufacture":"string",
            "ram":int,
            "cpu_ghz":float,
            "cpu_total":int,
            // Description of device result. If it is a functional test, you don't need to pay much attention to this information. You should focus on case results.
            "result": "string",
            // device result code
            // 0 for running, 1 for passed, 2 for has compatibility error, 3 for untest（caused by device exception, 4 for timeout, 5 for system canceled, 6 for user canceled
            "result_code": 0,
            // device process cost
            "cost_info":[{
            "process_name":"string", // process name means what device is doing
            "cost":int,              // cost time, unit is seconds
            "start_time":"string",   // start time of this process
            "end_time":"string"      // end time of this process
            }],
        },
        "msg": "string",
        "ret": int
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/tests/" + str(test_id) + "/devices/" + str(device_id) + "?log=" + str(log) + "&image=" + str(image) + "&error=" + str(error)
    return curl_get(url)

def get_device_performance(test_id : int, device_id : int, type : str = "perf"):
    """
    curl -u <SecretId>:<SecretKey>  "https://api.paas.wetest.net/cloudtest/v1/tests/<test_id>/devices/<device_id>/metrics?type=perf"
    :param test_id: test id
    :param device_id: device id
    :param type: performance type, only support “perf” value now
    :return:{ 
        "data":[{
            "cpu_app": 8.0,         // CPU occupancy of tested app
            "cpu_total": 13.51,     // total CPU occupancy
            "fps": int,             // FPS
            "ios_memory": int,      // memory data of iOS app (MB)
            "label": "",            // Used to mark a piece of performance data
            "mem_native_pss": int,  // memory data of Android app (MB)
            "mem_pss": int,         // memory data of Android app (MB)
            "net_in": int,          // KB/s
            "net_out": int,         // KB/s
            "timestamp": int        // unix timestamp
        }],
        "msg": "string",
        "ret": int
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/tests/" + str(test_id) + "/devices/" + str(device_id) + "/metrics?type=" + str(type)
    return curl_get(url)

def get_test_summary(test_id : int):
    """
    curl -u <SecretId>:<SecretKey>  "https://api.paas.wetest.net/cloudtest/v1/tests/<test_id>/result"
    :param test_id: test id
    :return:{
        "msg": "string",
        "ret": int,
        "test_result": {
            // start time of test
            "start_time": "string",
            // end time of test
            "end_time": "string",
            // test frame type
            "frame_type_code": int, 
            // test frame type
            "frame_type": "string",
            // report url to view details of test result
            "report_url": "string",
            // test status,0 for testing,1 for finished,2 for canceled,3 for timeout
            "status_code": int,
            // test status description
            "status":"string",
            "test_id": int,
            "test_type": "string",
            "test_type_code": int,
            // tested app info
            "app_info": {
            "app_type": "android",
            "icon_url": "string",
            "name": "string",
            "package": "string",
            "size": int,
            "version": "string"
            },
            // result of device dimension
            "result_stat": {
            "total_device_number": int,
            "pass_device_number": int,
            "exception_device_number": int,
            "in_process_device_number": int,
            "fist_start_device_time": "string",
            // maximum waiting time
            "max_wait_time": int,
            // minimum waiting time
            "min_wait_time": int,
            // last device launched time
            "last_start_device_time": "string",
            "pass_rate": float,
            "exception_rate": float,
            }
        }
    }
    """
    url = "https://api.paas.wetest.net/cloudtest/v1/tests/" + str(test_id) + "/result"
    return curl_get(url)

def save_all_devices(json_file : str = "devices.json"):
    status, result, reason = get_devices()
    if status != 200:
        print("get devices failed, status: " + status + " reason: " + str(reason))
    else:
        with open(json_file, "w") as f:
            json.dump(result, f)
            print("save devices success")

def get_tests_details(test_ids:list, file_name : str = "test_details.xlsx"):
    """
    获取所有测试的详细信息, 写入到指定的excel文件中
    """
    import openpyxl
    import math
    import os
    try:
        import tqdm
    except ImportError:
        os.system("pip3 install tqdm")
        import tqdm

    folder = os.path.dirname(file_name)
    if folder != "" and not os.path.exists(folder):
        os.makedirs(folder)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["device id", "test id", "report url", "test result", "case success", "case total", "model", "os version", "manufacture", "ram(M)", "cpu_ghz(G)", "cpu_total(G)", "cpu_app_avg(%)", "fps_avg", "mem_native_pss_avg(M)", "mem_pss_avg(M)", "net_in_avg(K)", "net_out_avg(K)"])
    for test_id in tqdm.tqdm(test_ids):
        test_url = "https://console.wetest.net/app/testlab/automation/report/" + str(test_id) + "/"
        print("test id: " + str(test_id))
        status, result, reason = get_test_results(test_id)
        if status != 200:
            print(test_id)
            print("get test summary failed, status: " + status + " reason: " + str(reason))
        else:
            devices = result["devices"]
            for device in devices:
                device_id = device["device_id"]
                case_url = test_url + "device/" + str(device_id)
                status, deviceInfo, reason = get_device_test_result(test_id, device_id)
                if status != 200:
                    print(device["device_id"])
                    print("get device test result failed, status: " + status + " reason: " + str(reason))
                    continue
                status, devicePerformance, reason = get_device_performance(test_id, device_id)
                if status != 200:
                    print(device["device_id"])
                    print("get device performance failed, status: " + status + " reason: " + str(reason))
                    continue
                test_details = deviceInfo["device"]
                perf_details = devicePerformance["data"]
                case_success = test_details["case_stat"]["case_success"]
                case_total = test_details["case_stat"]["case_total"]
                test_result = test_details["result"]
                model = test_details["model"]
                version = test_details["version"]
                manufacture = test_details["manufacture"]
                ram = test_details["ram"]
                cpu_ghz = test_details["cpu_ghz"]
                cpu_total = test_details["cpu_total"]
                cpu_app = []
                fps = []
                #ios_memory = []
                mem_native_pss = []
                mem_pss = []
                net_in = []
                net_out = []
                timestamp = []
                for perf in perf_details:
                    cpu_app.append(perf["cpu_app"])
                    fps.append(perf["fps"])
                    #ios_memory.append(perf["ios_memory"])
                    mem_native_pss.append(perf["mem_native_pss"])
                    mem_pss.append(perf["mem_pss"])
                    net_in.append(perf["net_in"])
                    net_out.append(perf["net_out"])
                    timestamp.append(perf["timestamp"])

                cpu_app_avg = sum(cpu_app) / len(cpu_app) if len(cpu_app) > 0 else 0
                fps_avg = sum(fps) / len(fps) if len(fps) > 0 else 0
                #ios_memory_avg = sum(ios_memory) / len(ios_memory) if len(ios_memory) > 0 else 0
                mem_native_pss_avg = sum(mem_native_pss) / len(mem_native_pss) if len(mem_native_pss) > 0 else 0
                mem_pss_avg = sum(mem_pss) / len(mem_pss) if len(mem_pss) > 0 else 0
                net_in_avg = sum(net_in) / len(net_in) if len(net_in) > 0 else 0
                net_out_avg = sum(net_out) / len(net_out) if len(net_out) > 0 else 0

                this_line = [str(device_id), str(test_id), case_url, test_result, case_success, case_total, model, version, manufacture, ram, cpu_ghz, cpu_total, cpu_app_avg, fps_avg, mem_native_pss_avg, mem_pss_avg, net_in_avg * 1024, net_out_avg * 1024]
                print(this_line)
                ws.append(this_line)

    wb.save(filename=file_name)

def upload_app_for_test(app_path : str, script_id : int):
    import os
    app_name = os.path.basename(app_path)
    status, result, reason = upload_app(app_name, app_path)
    if status != 200:
        print("upload app failed, status: " + status + " reason: " + str(reason))
    else:
        print(result)
        app_id = result["data"]["fid"]
        print("upload app success, app_id: " + str(app_id))
        status, result, reason = submit_test(app_id, script_id, 5)
        if status != 200:
            print("submit test failed, status: " + status + " reason: " + str(reason))
        else:
            print(result)
            print("submit test success, test_id: " + str(result["test_info"]["test_id"]))
            print("test url: " + "https://console.wetest.net/app/testlab/automation/report/" + str(result["test_info"]["test_id"]) + "/")

if __name__ == "__main__":
    # print(upload_script(r"xxx.zip"))
    # upload_app_for_test(r"xxx.apk", 34433)
    # print(get_app("YEQDOaq3"))
    # print(get_script(34433))
    # print(submit_test("YEQDOaq3", 34357, 5))
    # print(get_test_status(2023052500317458))
    # print(get_test_results(2023052600620231))
    # print(get_device_test_result(2023052600620231, 10132))
    # save_all_devices()
    # print(get_test_results(2023071400392688))
    # status, result, reason = get_test_results(2023071400392688)
    # # print(len(result["devices"]))
    # count = 0
    # for dev in result["devices"]:
    #     if dev["result"] == "testing":
    #         count += 1
    #     print(str(count) + " " + dev["result"] + " " + str(dev["device_id"]))
    print(cancel_test(2024052700413513))
    # get_tests_details([2023121500854210, 2023121500854420, 2023121500654658, 2023121500554787, 2023121500754919, 2023121500155023, 2023121600955101, 2023121600655878, 2023121600056332, 2023121800658428, 2023121800358675, 2023121800058952, 2023121800659148])