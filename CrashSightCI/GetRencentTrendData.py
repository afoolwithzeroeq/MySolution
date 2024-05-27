import datetime

from Define import *
from CrashSightAPI import *

def get_rate_message(rate : float):
    if rate >= 3:
        return warning_message(str(rate))
    else:
        return info_message(str(rate))

class OneTrendData:
    def __init__(self):
        self.accessNum = 0
        self.accessUser = 0
        self.crashNum = 0
        self.crashUser = 0
    def Add(self, accessNum, accessUser, crashNum, crashUser):
        self.accessNum += accessNum
        self.accessUser += accessUser
        self.crashNum += crashNum
        self.crashUser += crashUser

def GetRencentTrendData(platform : Platform, channel : Channel, version : str, days : int = 1):
    """
    获取CrashSight最近N天的趋势数据
    :param days: 最近N天
    """
    api = CrashsightOpenApi(platform, channel, version)
    date = datetime.datetime.now()
    endDate = date.strftime("%Y%m%d")
    startDate = (date - datetime.timedelta(days=days - 1)).strftime("%Y%m%d")
    print("startDate: ", startDate)
    print("endDate: ", endDate)
    if channel == Channel.Global:
        result = api.get_trend_ex(Type.Crash, startDate, endDate, True, OpenAllCountries)
    else:
        result = api.get_trend_ex(Type.Crash, startDate, endDate)
    trendDatas : dict[str, OneTrendData] = {}
    for item in result:
        if item.date not in trendDatas:
            trendDatas[item.date] = OneTrendData()
        trendDatas[item.date].Add(item.accessNum, item.accessUser, item.crashNum, item.crashUser)

    message = "**平台**: " + platform + "  **渠道**: " + channel + "  **版本**: " + version + "\n"
    for key in trendDatas:
        result = trendDatas[key]
        message += "> (" + datetime.datetime.strptime(key, "%Y%m%d").strftime("%Y-%m-%d") + ")"
        if result.accessUser == 0:
            message += " **设备崩溃率**: " + get_rate_message(0) + "%  " + comment_message("(0/0)") + "\n"
        else:
            message += " **设备崩溃率**: " + get_rate_message(round(result.crashUser / result.accessUser * 100, 2)) + "%  " + comment_message("(" + str(result.crashUser) + "/" + str(result.accessUser) + ")") + "\n"

    message += "\n"
    return message

def GetRencentTrendDataTask():
    message = "## CrashSight崩溃数据\n"
    for version in VersionList:
        message += "--------------------\n"
        message += GetRencentTrendData(version.platform, version.channel, version.version, 3)

    message += "--------------------\n"
    message += "说明: " + comment_message("设备崩溃率%  (崩溃设备数/启动设备数)") + "\n"
    print(message)
    send_wechat_message(message, "markdown", web_key)

if __name__ == "__main__":
    GetRencentTrendDataTask()