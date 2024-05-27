import datetime

from Define import *
from CrashSightAPI import *

def GetDailyRealTimeData(platform : Platform, channel : Channel, version : str):
    """
    获取CrashSight单日累计实时数据
    """
    api = CrashsightOpenApi(platform, channel, version)
    date = datetime.datetime.now()
    startHour = date.strftime("%Y%m%d00")
    endHour = date.strftime("%Y%m%d%H")
    print("startHour: ", startHour)
    print("endHour: ", endHour)
    result = api.get_real_time_append_stat_get(Type.Crash, startHour, endHour)[0]
    print(result)
    message = "## CrashSight单日累计实时数据\n"
    message += "**日期**: " + date.strftime("%Y-%m-%d-%H") + "\n"
    message += "**平台**: " + platform + "\n"
    message += "**渠道**: " + channel + "\n"
    message += "**版本**: " + version + "\n"
    message += "**启动次数**: 真机:" + str(result.accessNum - result.vmAccessNum) + " 模拟器:" + str(result.vmAccessNum) + "\n"
    message += "**联网设备数**: 真机:" + str(result.accessUser - result.vmAccessUser) + " 模拟器:" + str(result.vmAccessUser) + "\n"
    message += "**崩溃次数**: 真机:" + str(result.crashNum - result.vmCrashNum) + " 模拟器:" + str(result.vmCrashNum) + "\n"
    message += "**次数崩溃率**: 真机:" + str(round((result.crashNum - result.vmCrashNum) / (result.accessNum - result.vmAccessNum) * 100, 2)) + "% 模拟器:" + str(round(result.vmCrashNum / result.vmAccessNum * 100, 2)) + "%\n"
    message += "**崩溃设备数**: 真机:" + str(result.crashUser - result.vmCrashUser) + " 模拟器:" + str(result.vmCrashUser) + "\n"
    message += "**设备崩溃率**: 真机:" + str(round((result.crashUser - result.vmCrashUser) / (result.accessUser - result.vmAccessUser) * 100, 2)) + "% 模拟器:" + str(round(result.vmCrashUser / result.vmAccessUser * 100, 2)) + "%\n"
    print(message)
    send_wechat_message(message, "markdown")

if __name__ == "__main__":
    GetDailyRealTimeData(Platform.Android, Channel.Global, "0.6.13547.798")