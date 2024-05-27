# coding: utf-8
import requests
import time
import base64
import hmac
import hashlib
import urllib3
import json
from typing import List

from Define import *
from Settings import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_wechat_message(content : str, msg_type : str = "text", web_key = "xxxx"):
    """
    默认的机器人是测试机器人
    """
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + web_key
    data = {"msgtype": msg_type, msg_type: {"content": content}}
    r = requests.post(url=webhook_url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    return r.text, r.status_code

def warning_message(content):
    return "<font color=\"warning\">{}</font>".format(content)

def info_message(content):
    return "<font color=\"info\">{}</font>".format(content)

def comment_message(content):
    return "<font color=\"comment\">{}</font>".format(content)

class CrashsightOpenApi(object):
    """
    由[Crashsight OpenAPI](https://apifox.com/apidoc/shared-1cd08bfa-0dd6-4027-9bf5-fec44e5c8481)提供的接口封装
    """
    def __init__(self, platform : Platform, channel : Channel, version : str = "-1"):
        """
        :param platform: 平台(Android, iOS, PC)
        :param channel: 渠道(Global, China)
        :param version: 版本号
        """
        self.headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding':'*'
        }
        self.platform = platform
        self.channel = channel
        self.localUserId = LocalUserId[channel]
        self.userOpenapiKey = UserOpenapiKey[channel]
        self.request_url = RequestUrl[channel]
        self.platformId = PlatformId[platform]
        self.appId = AppId[channel][platform]
        self.version = version
        self.versionList = None if version == "-1" else [version]


        # 获取当前时间戳
        self.t = int(time.time())

    def __get_api_signature(self):
        """
        获取签名计算值的方法
        """
        key_bytes = bytes(self.userOpenapiKey, 'utf-8')
        message = self.localUserId + '_'+ str(self.t)
        message_bytes = bytes(message, 'utf-8')
        hash_str = hmac.new(key_bytes, message_bytes, digestmod=hashlib.sha256).hexdigest()
        # print(hash_str)

        hash_str_64 = base64.b64encode(bytes(hash_str, encoding="utf8"))
        hash_str_64 = str(hash_str_64, encoding="utf-8")
        # print(hash_str_64)

        return hash_str_64

    def do_post_request(self, methodName, body):
        """
        获取相关的接口返回数据
        """
        if body.get("version") is not None:
            if body.get("version").find("*") != -1:
                body["mergeMultipleVersionsWithInaccurateResult"] = True
        request_url = self.request_url + methodName + ('?userSecret={}&localUserId={}&t={}'.format(self.__get_api_signature(), self.localUserId, str(self.t)))
        print(request_url)
        print(json.dumps(body))
        content = requests.post(request_url, data = json.dumps(body), headers = self.headers).content
        if content is None:
            return None
        
        result = json.loads(content)
        if result["status"] != 200:
            print(result)
            return None
        if result.get("data") is not None:
            return result.get("data")
        if result.get("ret") is not None:
            if result["ret"].get("data") is not None:
                return result["ret"]["data"]
            else:
                return result["ret"]
        return result
    
    def do_get_request(self, methodName, body):
        """
        获取相关的接口返回数据
        """
        if body.get("version") is not None:
            if body.get("version").find("*") != -1:
                body["mergeMultipleVersionsWithInaccurateResult"] = True
        # 对于get请求，将body参数拼接到url中
        request_url = self.request_url + methodName
        for key in body:
            request_url += ('/{}/{}'.format(key, body[key]))
        request_url = request_url + ('?fsn=4d8a5f7f-935e-4d7a-be35-d4edb2424fb5&userSecret={}&localUserId={}&t={}'.format(self.__get_api_signature(), self.localUserId, str(self.t)))
        print(request_url)

        content = requests.get(request_url, headers=self.headers, verify=False).content
        if content is None:
            return None
        result = json.loads(content)
        if result["status"] != 200:
            print(result)
            return None
        if result.get("data") is not None:
            return result.get("data")
        return result["ret"]["data"]

    def get_trend_ex(self, type : Type, startDate : str, endDate : str, needCountryDimension : bool = None, countryList : List[str] = None, mergeMultipleVersionsWithInaccurateResult : bool = None) -> List[TrendExData]:
        """
        获取趋势数据(最近N天)
        :param type: 数据类型
        :param startDate: 开始时间 YYMMDDHH
        :param endDate: 结束时间 YYMMDDHH
        :param needCountryDimension: true: 需要国家维度的统计 false: 不需要
        :param countryList: 如果设置了需要国家维度的统计，则传入需要查询的国家名称列表。如果设置了needCountryDimension但countryList为空数组，则表示查询全部国家地区
        :param mergeMultipleVersionsWithInaccurateResult: 多版本的结果是否要合并成一条结果。合并方式为所有单个版本的设备数、次数直接相加。
        """
        body = {
            "appId": self.appId,
            "platformId": self.platformId,
            "type": type,
            "dataType": "trendData",
            "vm": VMType.Real,
            "startDate": startDate,
            "endDate": endDate,
        }
        if needCountryDimension is not None:
            body["needCountryDimension"] = needCountryDimension
        if countryList is not None:
            body["countryList"] = countryList
        if mergeMultipleVersionsWithInaccurateResult is not None:
            body["mergeMultipleVersionsWithInaccurateResult"] = mergeMultipleVersionsWithInaccurateResult
        if self.versionList is not None:
            body["versionList"] = self.versionList

        return [TrendExData(data) for data in self.do_post_request("getTrendEx", body)]

    def fetch_dimension_top_stats(self, type : Type, minDate : str, maxDate : str, limit : int = 5, field : Field = Field.Version, mergeMultipleVersionsWithInaccurateResult = False, sortByException = True, needCountryDimension : bool = None, countryList : List[str] = None, mergeMultipleDatesWithInaccurateResult : bool = False) -> List[FimensionTopStatsData]:
        """
        崩溃、ANR、错误类型的排行榜接口(影响设备数/设备崩溃率/联网设备数)
        :param type: 数据类型
        :param minDate: 开始时间 YYYYMMDD
        :param maxDate: 结束时间 YYYYMMDD
        :param version: 版本。版本支持通配符
        :param limit: 条数限制
        :param field: 聚合维度
        :param mergeMultipleVersionsWithInaccurateResult: 多版本的结果是否要合并成一条结果。合并方式为所有单个版本的设备数、次数直接相加。
        :param sortByException: 排序标识
        :param needCountryDimension: 是否需要国家维度的统计
        :param countryList: 如果设置了需要国家维度的统计，则传入需要查询的国家名称列表。如果设置了needCountryDimension但countryList为空数组，则表示查询全部国家地区
        :param mergeMultipleDatesWithInaccurateResult: 多天的结果是否要合并成一条结果。合并方式为所有单个日期的设备数、次数直接相加。
        """
        body = {
            "appId": self.appId,
            "platformId": self.platformId,
            "type": type,
            "minDate": minDate,
            "maxDate": maxDate,
            "version": self.version,
            "limit": limit,
            "field": field,
            "mergeMultipleVersionsWithInaccurateResult": mergeMultipleVersionsWithInaccurateResult,
            "sortByException": sortByException,
            "mergeMultipleDatesWithInaccurateResult": mergeMultipleDatesWithInaccurateResult,
        }
        if needCountryDimension is not None:
            body["needCountryDimension"] = needCountryDimension
        if countryList is not None:
            body["countryList"] = countryList
        if mergeMultipleVersionsWithInaccurateResult is not None:
            body["mergeMultipleVersionsWithInaccurateResult"] = mergeMultipleVersionsWithInaccurateResult

        return [FimensionTopStatsData(data) for data in self.do_post_request("fetchDimensionTopStats", body)]

    def get_top_issue_hourly(self, type : Type, startHour : str, limit : int = 5, topIssueDataType : str = "", needCountryDimension : bool = None, countryList : List[str] = None) -> List[TopIssueHourly]:
        """
        小时级TOP问题列表
        :param type: 数据类型
        :param startHour: 开始时间 YYYYMMDDHH
        :param limit: 条数限制
        :param topIssueDataType: 排行榜类型
        :param needCountryDimension: 是否需要国家维度的统计
        :param countryList: 如果设置了需要国家维度的统计，则传入需要查询的国家名称列表。如果设置了needCountryDimension但countryList为空数组，则表示查询全部国家地区
        """
        body = {
            "appId": self.appId,
            "platformId": self.platformId,
            "version": self.version,
            "type": type,
            "startHour": startHour,
            "limit": limit,
            "topIssueDataType": topIssueDataType,
        }
        if needCountryDimension is not None:
            body["needCountryDimension"] = needCountryDimension
        if countryList is not None:
            body["countryList"] = countryList

        return TopIssueHourly(self.do_post_request("getTopIssueHourly", body))

    def get_real_time_append_stat(self, type : Type, startHour : str, endHour : str) -> List[RealTimeAppendStat]:
        """
        [暂不可用](https://apifox.com/apidoc/shared-1cd08bfa-0dd6-4027-9bf5-fec44e5c8481/api-165640177)(post)获取单日的异常概览数据：崩溃，ANR，卡顿，错误
        :param startHour: 格式YYYYMMDDHH，小时的部分必须是00
        :param endHour: 格式YYYYMMDDHH，必须和startHour是同一天
        :param type: 数据类型
        """
        if not startHour.endswith("00"):
            print("startHour的小时部分必须是00")
            return None
        if startHour[0:8] != endHour[0:8]:
            print("startHour和endHour不是同一天")
            return None
        body = {
            "appId": self.appId,
            "platformId": self.platformId,
            "version": self.version,
            "startHour": startHour,
            "endHour": endHour,
            "type": type,
            "fsn": "4d8a5f7f-935e-4d7a-be35-d4edb2424fb5",
        }

        return [RealTimeAppendStat(data) for data in self.do_post_request("getRealTimeAppendStat", body)]

    def get_real_time_append_stat_get(self, type : Type, startHour : str, endHour : str) -> List[RealTimeAppendStat]:
        """
        (get)获取单日的异常概览数据：崩溃，ANR，卡顿，错误
        :param startHour: 格式YYYYMMDDHH，小时的部分必须是00
        :param endHour: 格式YYYYMMDDHH，必须和startHour是同一天
        :param type: 数据类型
        """
        if not startHour.endswith("00"):
            print("startHour的小时部分必须是00")
            return None
        if startHour[0:8] != endHour[0:8]:
            print("startHour和endHour不是同一天")
            return None
        body = {
            "appId": self.appId,
            "platformId": self.platformId,
            "version": self.version,
            "startHour": startHour,
            "endHour": endHour,
            "type": type,
        }

        return [RealTimeAppendStat(data) for data in self.do_get_request("getRealTimeAppendStat", body)]

    def advanced_search_ex(self, type : Type, startHour : str, endHour : str) -> List[AdvancedSearchEx]:
        """
        [暂不可用](https://apifox.com/apidoc/shared-1cd08bfa-0dd6-4027-9bf5-fec44e5c8481/api-139597918)崩溃分析自定义检索
        :param type: 数据类型
        :param startHour: 开始时间 YYYYMMDDHH
        :param endHour: 结束时间 YYYYMMDDHH
        """
        body = {
            "appId": self.appId,
            "platformId": self.platformId,
            "type": type,
            "dataType": "realTimeTrendData",
            "startHour": startHour,
            "endHour": endHour,
        }

        return [AdvancedSearchEx(data) for data in self.do_post_request("advancedSearchEx", body)]

    def get_app_real_time_trend_append_ex(self, type : Type, startHour : str, endHour : str, vmType : VMType = VMType.Real, needCountryDimension : bool = None, countryList : List[str] = None, mergeMultipleVersionsWithInaccurateResult : bool = None) -> List[AppRealTimeTrendAppendEx]:
        """
        获取趋势数据(今天-累计)
        :param type: 数据类型
        :param startHour: 开始时间 YYYYMMDDHH
        :param endHour: 结束时间 YYYYMMDDHH
        :param vmType: VM类型
        :param needCountryDimension: 是否需要国家维度的统计
        :param countryList: 如果设置了需要国家维度的统计，则传入需要查询的国家名称列表。如果设置了needCountryDimension但countryList为空数组，则表示查询全部国家地区
        """
        body = {
            "appId": self.appId,
            "platformId": self.platformId,
            "type": type,
            "dataType": "realTimeTrendData",
            "startDate": startHour,
            "endDate": endHour,
            "vm": vmType,
            "versionList": self.versionList,
        }
        if needCountryDimension is not None:
            body["needCountryDimension"] = needCountryDimension
        if countryList is not None:
            body["countryList"] = countryList
        if mergeMultipleVersionsWithInaccurateResult is not None:
            body["mergeMultipleVersionsWithInaccurateResult"] = mergeMultipleVersionsWithInaccurateResult

        return [AppRealTimeTrendAppendEx(data) for data in self.do_post_request("getAppRealTimeTrendAppendEx", body)]

    def get_real_time_hourly_stat_ex(self):
        """
        (todo)获取趋势数据(今天-按小时)
        """
        return self.do_post_request("getRealTimeHourlyStatEx", {})
    
    def add_tag(self, issueId : str, tag : str):
        """
        (todo)设置问题标签
        """
        return self.do_post_request("addTag", {})
    
    def advanced_search(self):
        """
        (todo)崩溃分析高级搜索
        """
        return self.do_post_request("advancedSearch", {})

    def query_access_list(self):
        """
        (todo)用户最近3日异常数据上报
        """
        return self.do_post_request("queryAccessList", {})
    
    def get_stack_device_info(self):
        """
        (todo)根据堆栈关键字获取机型列表(国内)
        """
        return self.do_post_request("getStackDeviceInfo", {})
    
    def get_crash_user_list(self):
        """
        (todo)获取时间段内崩溃用户列表
        """
        return self.do_post_request("getCrashUserList", {})
    
    def get_stack_crash_stat(self):
        """
        (todo)根据堆栈关键字获取崩溃统计
        """
        return self.do_post_request("getStackCrashStat", {})
    
    def get_crash_device_stat(self):
        """
        (todo)根据deviceId获取崩溃列表(移动端)
        """
        return self.do_post_request("getCrashDeviceStat", {})
    
    def get_crash_device_info(self):
        """
        (todo)根据issue获取时间段crashHash列表
        """
        return self.do_post_request("getCrashDeviceInfo", {})
    
    def get_device_user_info(self):
        """
        (todo)根据设备id获取OpenId
        """
        return self.do_post_request("getDeviceUserInfo", {})
    
    def note_list_get(self):
        """
        (todo)(get)获取某一个issue下的note
        """
        return self.do_get_request("noteList", {})
    
    def note_list(self):
        """
        (todo)(post)获取某一个issue下的note
        """
        return self.do_post_request("noteList", {})
    
    def issue_info_get(self):
        """
        (todo)(get)获取issue详情
        """
        return self.do_get_request("issueInfo", {})
    
    def issue_info(self):
        """
        (todo)(post)获取issue详情
        """
        return self.do_post_request("issueInfo", {})
    
    def crash_list_get(self):
        """
        (todo)(get)根据issue获取crashHash列表 (支持PC)
        """
        return self.do_get_request("crashList", {})
    
    def crash_list(self):
        """
        (todo)(post)根据issue获取crashHash列表 (支持PC)
        """
        return self.do_post_request("crashList", {})

    def last_crash_info_get(self):
        """
        (todo)(get)根据issue获取最近一次crashHash(支持PC)
        """
        return self.do_get_request("lastCrashInfo", {})
    
    def last_crash_info(self):
        """
        (todo)(post)根据issue获取最近一次crashHash(支持PC)
        """
        return self.do_post_request("lastCrashInfo", {})
    
    def app_detail_crash_get(self):
        """
        (todo)(get)获取跟踪数据，跟踪日志，其他信息，自定义kv等
        """
        return self.do_get_request("appDetailCrash", {})
    
    def app_detail_crash(self):
        """
        (todo)(post)获取跟踪数据，跟踪日志，其他信息，自定义kv等
        """
        return self.do_post_request("appDetailCrash", {})
    
    def crash_doc_get(self):
        """
        (todo)(get)获取崩溃详情(支持PC)
        """
        return self.do_get_request("crashDoc", {})
    
    def crash_doc(self):
        """
        (todo)(post)获取崩溃详情(支持PC)
        """
        return self.do_post_request("crashDoc", {})
    
    def query_issue_list(self, rows = 10, exceptionTypeList : str = "Crash,Native", sortOrder = "desc", status : str = None, sortField = "uploadTime", date : str = None):
        """
        崩溃分析，ANR分析，错误分析(支持PC)
        :param rows: 获取条数
        :param exceptionTypeList: 异常类型数组，逗号分隔多个值。支持的异常类型有：Crash, Native, AllCatched, ANR, Unity3D, AllCrash, ExtensionCrash, Lua, JS
        :param sortOrder: 排序顺序。可选值：desc, asc
        :param status: 问题状态。可选，按照问题处理状态过滤 0：未处理 1： 已处理 2： 处理中 支持多选，用英文逗号连接，例如 0,2 表示过滤未处理或处理中 参数示例： 0
        :param sortField: 排序字段
        :param date: 按照问题最近时间段过滤。注意参与过滤的属性是问题的最近上报时间，而不是上报的时间。不传这个字段就是所有时间 \n last_1_hour(最近1小时) \n last_2_day(最近2天) \n last_7_day(最近7天) \n last_15_day(最近15天) \n last_30_day(最近30天)
        """
        body = {
            "appId": str(self.appId),
            "platformId": self.platformId,
            "version": self.version,
            "rows": rows,
            "exceptionTypeList": exceptionTypeList,
            "sortOrder": sortOrder,
            "sortField": sortField,
            "skipQueryHbase": True,
        }
        if status is not None:
            body["status"] = status
        if date is not None:
            body["date"] = date


        return QueryIssueList(self.do_post_request("queryIssueList", body))
    
    def get_top_issue_get(self):
        """
        (todo)(get)TOP问题列表
        """
        return self.do_get_request("getTopIssue", {})
    
    def get_top_issue_ex(self):
        """
        (todo)(post)TOP问题列表
        """
        return self.do_post_request("getTopIssueEx", {})
    
    def query_crash_list(self):
        """
        (todo)(post)上报详情条件查询
        """
        return self.do_post_request("queryCrashList", {})
    
    def upsert_bugs(self, bugs : List[BugIssue]):
        """
        创建缺陷单
        """
        body = {
            "appId": self.appId,
            "platformId": self.platformId,
        }
        issueList = []
        for bug in bugs:
            issue = {
                "issueHash": bug.issueHash,
                "bugInfoList": [
                    {
                        "status": "new",
                        "titleBase64": bug.title,
                        "descriptionBase64": bug.description,
                        "reporter": bug.reporter,
                        "includeAttachments": True,
                        "attachmentFilenameList": [],
                        "severity": "normal",
                        "currentOwner": bug.currentOwner,
                    },
                ],
            }
            issueList.append(issue)
        body["issueList"] = issueList

        return self.do_post_request("upsertBugs", body)
    
    def update_issue_status(self):
        """
        (todo)更新issue状态接口
        """
        return self.do_post_request("updateIssueStatus", {})
    
    def get_crash_device_info_by_expuid(self):
        """
        (todo)根据expUid获取机型列表(移动端)
        """
        return self.do_post_request("getCrashDeviceInfoByExpUid", {})
    
    def add_issue_note(self):
        """
        (todo)添加问题备注
        """
        return self.do_post_request("addIssueNote", {})
    
    def get_version_date_list(self):
        """
        (todo)获取系统保存的版本号首次出现的日期(个别项目通用获取使用，数据被清理时数据会变动)
        """
        return self.do_post_request("getVersionDateList", {})
    
    def get_selector_datas_get(self, types : str = "member"):
        """
        (get)获取版本，包名，处理人等列表(支持PC)
        """
        body = {
            "appId": self.appId,
            "pid": str(self.platformId),
            "types": types,
            "fsn": "4d8a5f7f-935e-4d7a-be35-d4edb2424fb5",
        }
        return self.do_get_request("getSelectorDatas", body)
    
    def get_selector_datas(self, types : str = "member"):
        """
        (post)获取版本，包名，处理人等列表(支持PC)
        """
        body = {
            "appId": self.appId,
            "pid": str(self.platformId),
            "types": types,
            "fsn": "4d8a5f7f-935e-4d7a-be35-d4edb2424fb5",
        }

        return self.do_post_request("getSelectorDatas", body)
    
    def get_crash_user_info(self):
        """
        (todo)根据openid获取用户崩溃详情
        """
        return self.do_post_request("getCrashUserInfo", {})

if __name__ == "__main__":
    version = "0.6.13547.798"
    # version = "-1"
    crashsight_open_api_obj = CrashsightOpenApi(Platform.Android, Channel.Global, version)
    result = crashsight_open_api_obj.get_selector_datas_get()
    if isinstance(result, list):
        for data in result:
            print(data)
    else:
        print(result)
    
