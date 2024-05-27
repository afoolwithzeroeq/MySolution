import datetime
from CrashSightAPI import *

class SpecError:
    label : str
    keyWords : List[str]
    maxIgnoreCount : int

    def __init__(self, label : str, keyWords : List[str], maxIgnoreCount : int = -1):
        self.keyWords = keyWords
        self.label = label
        self.maxIgnoreCount = maxIgnoreCount

SpecErrorList = [
    SpecError("NetMgr Default", ["NetMgr Default"]),
    SpecError("AssetBundle", ["[AssetManager]", 
                              "Failed to read data for the AssetBundle", 
                              "load prefab is null", 
                              "null prefab", 
                              "not built with the right version or build target.",
                              "cant load asset from",
                              "[DESIGN]can not load this atlas",
                              "has null object",
                              ], 20),
]

NumberList = [200, 20, 1, 0]
BugState = [True, False]

class IssueState:
    stateCount : List[List[int]]

    def __init__(self):
        self.stateCount = [[0 for i in range(len(BugState))] for j in range(len(NumberList))]

    def Merge(self, count : int, condition : bool):
        for i in range(len(NumberList)):
            if count > NumberList[i]:
                self.stateCount[i][condition] += 1
                return

    def Get(self, number : int, condition : bool = None):
        index = NumberList.index(number)
        if condition == None:
            return self.stateCount[index][True] + self.stateCount[index][False]
        else:
            return self.stateCount[index][condition]

def GetRecentErrorData(platform : Platform, channel : Channel, version : str, days : int = None):
    """
    获取CrashSight最近N天的错误数据
    :param days: 最近N天
    """
    api = CrashsightOpenApi(platform, channel, version)
    # date = datetime.datetime.now()
    # endDate = date.strftime("%Y%m%d")
    # startDate = (date - datetime.timedelta(days=days - 1)).strftime("%Y%m%d")
    # print("startDate: ", startDate)
    # print("endDate: ", endDate)
    if days == None:
        simple = api.query_issue_list(1, "Unity3D")#, date="last_"+ str(days) + "_day")#, status="0")
        print(simple.numFound)
        result = api.query_issue_list(simple.numFound, "Unity3D")#, date="last_"+ str(days) + "_day")
    else:
        simple = api.query_issue_list(1, "Unity3D", date="last_"+ str(days) + "_day")
        print(simple.numFound)
        result = api.query_issue_list(simple.numFound, "Unity3D", date="last_"+ str(days) + "_day")

    bugCount = 0
    issueCount = {}
    for spec in SpecErrorList:
        issueCount[spec.label] = 0
    deviceState = IssueState()
    countState = IssueState()
    for item in result.issueList:
        bSpec = False
        for spec in SpecErrorList:
            if spec.maxIgnoreCount == -1 or item.imeiCount <= spec.maxIgnoreCount:
                for key in spec.keyWords:
                    if item.exceptionMessage.find(key) != -1:
                        issueCount[spec.label] += 1
                        bSpec = True
                        break
            if bSpec:
                break
        if bSpec:
            continue
        bDeal = len(item.bugs) > 0 or item.status != 0
        if bDeal:
            bugCount += 1
        deviceState.Merge(item.imeiCount, bDeal)
        countState.Merge(item.count, bDeal)
    
    return simple.numFound, deviceState, countState, issueCount, bugCount

def GetErrorData():
    message = "## CrashSight错误数据 (" + datetime.datetime.now().strftime("%Y-%m-%d") + ")\n"
    for version in VersionList:
        message += "--------------------\n"
        message += "**平台**: " + version.platform + "  **渠道**: " + version.channel + "  **版本**: " + version.version + "\n"
        dayNum, dayDeviceState, dayCountState, dayIssueCount, dayBugCount = GetRecentErrorData(version.platform, version.channel, version.version, 1)
        totalNum, totalDeviceState, totalCountState, totalIssueCount, totalBugCount = GetRecentErrorData(version.platform, version.channel, version.version)
        message += "> **今日错误数**: " + comment_message(str(dayNum) + "/" + str(totalNum))
        dayOtherCount, totalOtherCount = dayNum, totalNum
        for spec in SpecErrorList:
            dayOtherCount -= dayIssueCount[spec.label]
            totalOtherCount -= totalIssueCount[spec.label]
            message += "  " + spec.label + ": " + comment_message(str(dayIssueCount[spec.label]) + "/" + str(totalIssueCount[spec.label]))
        message += "  其它: " + comment_message(str(dayOtherCount) + "/" + str(totalOtherCount) + "(" + info_message(str(dayBugCount) + "/" + str(totalBugCount) + ")")) + "\n"
        message += "**影响设备数**: 等于1: " + comment_message(str(dayDeviceState.Get(0)) + "/" + str(totalDeviceState.Get(0)) + "(" + str(dayDeviceState.Get(0, True)) + "/" + str(totalDeviceState.Get(0, True)) + ")")
        message += "  大于1: " + comment_message(str(dayDeviceState.Get(1)) + "/" + str(totalDeviceState.Get(1)) + "(" + str(dayDeviceState.Get(1, True)) + "/" + str(totalDeviceState.Get(1, True)) + ")")
        message += "  大于20: " + warning_message(str(dayDeviceState.Get(20)) + "/" + str(totalDeviceState.Get(20))) + "(" + info_message(str(dayDeviceState.Get(20, True)) + "/" + str(totalDeviceState.Get(20, True))) + ")"
        message += "  大于200: " + warning_message(str(dayDeviceState.Get(200)) + "/" + str(totalDeviceState.Get(200))) + "(" + info_message(str(dayDeviceState.Get(200, True)) + "/" + str(totalDeviceState.Get(200, True))) + ")" + "\n"
        message += "\n"
    
    message += "--------------------\n"
    message += "说明: " + comment_message("今日数量/总计数量(今日处理中/总计处理中)") + "\n"
    print(message)
    send_wechat_message(message, "markdown", web_key)

if __name__ == "__main__":
    GetErrorData()