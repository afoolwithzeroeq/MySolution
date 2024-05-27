from Settings import *
from CrashSightAPI import *

def SendDutyMessage():
    message = "## 线上值班\n"
    for version in VersionList:
        message += "**版本**: " + version.version + "  平台: " + version.platform + "  渠道: " + version.channel + "\n"
    message += "**值班人员**: "
    for duty in DutyMan:
        message += "<@" + duty + "> "
    print(message)
    send_wechat_message(message, "markdown", "xxxx")

if __name__ == "__main__":
    SendDutyMessage()