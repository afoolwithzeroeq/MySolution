from CrashSightAPI import *
from Define import *

def AutoCreateBugs(version : Version, minDeviceCount : int = 20, minCount : int = 20):
    """
    todo: 自动创建Bug
    :param version: 版本信息
    :param minDeviceCount: 最小影响设备数
    :param minCount: 最小发生次数
    """

    api = CrashsightOpenApi(version.platform, version.channel, version.version)
    simple = api.query_issue_list(1, "Unity3D", status="0")
    print(simple.numFound)
    result = api.query_issue_list(simple.numFound, "Unity3D", status="0")

    createCount = 0
    for item in result.issueList:
        if item.imeiCount >= minDeviceCount or item.count >= minCount:
            createCount += 1
    
    print("createCount: ", createCount)

if __name__ == "__main__":
    AutoCreateBugs(VersionList[0], 20, 20)