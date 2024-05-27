from typing import List, Optional

class Platform:
    """平台(Android, iOS, PC)"""
    iOS = "iOS"
    Android = "Android"
    # PC = "PC"

class Channel:
    """渠道(Global, China)"""
    Global = "Global"
    China = "China"

class Version:
    """版本"""
    channel : Channel
    """渠道"""
    platform : Platform
    """平台"""
    version : str
    """版本"""

    def __init__(self, channel, platform, version):
        self.channel = channel
        self.platform = platform
        self.version = version

class Type:
    """数据类型(Crash, ANR, Error)"""
    Crash = "crash"
    ANR = "anr"
    Error = "error"

class Field:
    """聚合维度(Version, Model, osVersion)"""
    Model = "model"
    """设备"""
    osVersion = "osVersion"
    """系统版本"""
    Version = "version"
    """应用版本"""

class VMType:
    """真机统计类型(All, Real, VM)"""
    All = 0
    """全量"""
    Real = 1
    """真机"""
    VM = 2
    """模拟器"""

class BaseData:
    def __str__(self) -> str:
        return str(self.__dict__)

class TrendExData(BaseData):
    """
    趋势数据
    """
    accessNum: int
    """联网次数"""
    accessUser: int
    """联网用户数"""
    appId: str
    """产品id"""
    country: str
    """国家"""
    crashNum: int
    """崩溃次数"""
    crashUser: int
    """崩溃用户数"""
    date: str
    """时间"""
    platformId: int
    """平台id"""
    reportDeviceAllData: int
    reportNumAllData: int
    version: str
    """项目版本"""

    def __init__(self, data):
        self.accessNum = data.get("accessNum")
        self.accessUser = data.get("accessUser")
        self.appId = data.get("appId")
        self.country = data.get("country")
        self.crashNum = data.get("crashNum")
        self.crashUser = data.get("crashUser")
        self.date = data.get("date")
        self.platformId = data.get("platformId")
        self.reportDeviceAllData = data.get("reportDeviceAllData")
        self.reportNumAllData = data.get("reportNumAllData")
        self.version = data.get("version")

class FimensionTopStatsData(BaseData):
    accessDevices: Optional[int]
    """联网设备数"""
    appId: Optional[str]
    """产品id"""
    date: Optional[str]
    """日期"""
    exceptionDevices: Optional[int]
    """影响设备数"""
    fieldValue: Optional[str]
    """维度值"""
    platformId: Optional[int]
    """平台id"""

    def __init__(self, data):
        self.accessDevices = data.get("accessDevices")
        self.appId = data.get("appId")
        self.date = data.get("date")
        self.exceptionDevices = data.get("exceptionDevices")
        self.fieldValue = data.get("fieldValue")
        self.platformId = data.get("platformId")

from typing import Optional, List


class IssueVersion(BaseData):
    count: Optional[int]
    deviceCount: Optional[int]
    firstUploadTimestamp: Optional[int]
    lastUploadTimestamp: Optional[int]
    systemExitCount: Optional[int]
    systemExitDeviceCount: Optional[int]
    version: Optional[str]

    def __init__(self, data) -> None:
        self.count = data.get("count")
        self.deviceCount = data.get("deviceCount")
        self.firstUploadTimestamp = data.get("firstUploadTimestamp")
        self.lastUploadTimestamp = data.get("lastUploadTimestamp")
        self.systemExitCount = data.get("systemExitCount")
        self.systemExitDeviceCount = data.get("systemExitDeviceCount")
        self.version = data.get("version")

class TopIssueList(BaseData):
    accumulateCrashNum: Optional[int]
    """累计影响次数"""
    accumulateCrashUser: Optional[int]
    """累计影响设备"""
    appId: Optional[str]
    """产品id"""
    crashNum: Optional[int]
    """发生次数"""
    crashUser: Optional[int]
    """影响设备数"""
    date: Optional[str]
    """时间"""
    exceptionMessage: Optional[str]
    """异常信息"""
    exceptionName: Optional[str]
    """异常类型"""
    firstUploadTime: Optional[str]
    """首次上报时间"""
    firstUploadTimestamp: Optional[int]
    issystemexit: Optional[bool]
    issueId: Optional[str]
    """问题issueId"""
    issueVersions: Optional[List[IssueVersion]]
    """issue版本集合"""
    keyStack: Optional[str]
    """堆栈信息"""
    lastUpdateTime: Optional[str]
    """最近更新时间"""
    lastUpdateTimestamp: Optional[int]
    platformId: Optional[int]
    """平台id"""
    preDayCrashNum: Optional[int]
    preDayCrashUser: Optional[int]
    prevHourCrashDevices: Optional[int]
    processors: Optional[str]
    """处理人"""
    state: Optional[int]
    """处理状态"""
    tags: Optional[List[str]]
    type: Optional[str]
    """类型"""
    version: Optional[int]
    """项目版本"""

    def __init__(self, data):
        self.accumulateCrashNum = data.get("accumulateCrashNum")
        self.accumulateCrashUser = data.get("accumulateCrashUser")
        self.appId = data.get("appId")
        self.crashNum = data.get("crashNum")
        self.crashUser = data.get("crashUser")
        self.date = data.get("date")
        self.exceptionMessage = data.get("exceptionMessage")
        self.exceptionName = data.get("exceptionName")
        self.firstUploadTime = data.get("firstUploadTime")
        self.firstUploadTimestamp = data.get("firstUploadTimestamp")
        self.issystemexit = data.get("issystemexit")
        self.issueId = data.get("issueId")
        self.issueVersions = [IssueVersion(issueVersion) for issueVersion in data.get("issueVersions")]
        self.keyStack = data.get("keyStack")
        self.lastUpdateTime = data.get("lastUpdateTime")
        self.lastUpdateTimestamp = data.get("lastUpdateTimestamp")
        self.platformId = data.get("platformId")
        self.preDayCrashNum = data.get("preDayCrashNum")
        self.preDayCrashUser = data.get("preDayCrashUser")
        self.prevHourCrashDevices = data.get("prevHourCrashDevices")
        self.processors = data.get("processors")
        self.state = data.get("state")
        self.tags = data.get("tags")
        self.type = data.get("type")
        self.version = data.get("version")

class TopIssueHourly(BaseData):
    accessDevices: int
    crashDevices: int
    preDayVersionCrashUser: int
    """前一天影响设备数量"""
    prevDaySameHourAccessDevices: int
    prevDaySameHourCrashDevices: int
    prevHourAccessDevices: int
    prevHourCrashDevices: int
    topIssueList: List[TopIssueList]
    versionCrashUser: int
    """影响设备数量"""

    def __init__(self, data) -> None:
        self.accessDevices = data.get("accessDevices")
        self.crashDevices = data.get("crashDevices")
        self.preDayVersionCrashUser = data.get("preDayVersionCrashUser")
        self.prevDaySameHourAccessDevices = data.get("prevDaySameHourAccessDevices")
        self.prevDaySameHourCrashDevices = data.get("prevDaySameHourCrashDevices")
        self.prevHourAccessDevices = data.get("prevHourAccessDevices")
        self.prevHourCrashDevices = data.get("prevHourCrashDevices")
        self.topIssueList = [TopIssueList(topIssue) for topIssue in data.get("topIssueList")]
        self.versionCrashUser = data.get("versionCrashUser")

class RealTimeAppendStat(BaseData):
    accessNum: int
    """联网次数"""
    accessUser: int
    """联网用户数"""
    anrNum: int
    """卡顿次数"""
    anrUser: int
    """卡顿用户数"""
    appId: str
    """产品id"""
    crashNum: int
    """崩溃次数"""
    crashUser: int
    """崩溃用户数"""
    date: str
    """时间"""
    errorNum: int
    """错误次数"""
    errorUser: int
    """错误用户数"""
    platformId: int
    """平台id"""
    type: str
    """类型"""
    version: str
    """项目版本"""
    vmAnrNum: int
    """模拟器卡顿次数"""
    vmAnrUser: int
    """模拟器卡顿用户数"""
    vmCrashNum: int
    """模拟器崩溃次数"""
    vmCrashUser: int
    """模拟器崩溃用户数"""
    vmErrorNum: int
    """模拟器错误次数"""
    vmErrorUser: int
    """模拟器错误用户数"""
    vmAccessNum: int
    """模拟器联网次数"""
    vmAccessUser: int
    """模拟器联网用户数"""

    def __init__(self, data):
        self.accessNum = data.get("accessNum")
        self.accessUser = data.get("accessUser")
        self.anrNum = data.get("anrNum")
        self.anrUser = data.get("anrUser")
        self.appId = data.get("appId")
        self.crashNum = data.get("crashNum")
        self.crashUser = data.get("crashUser")
        self.date = data.get("date")
        self.errorNum = data.get("errorNum")
        self.errorUser = data.get("errorUser")
        self.platformId = data.get("platformId")
        self.type = data.get("type")
        self.version = data.get("version")
        self.vmAnrNum = data.get("vmAnrNum")
        self.vmAnrUser = data.get("vmAnrUser")
        self.vmCrashNum = data.get("vmCrashNum")
        self.vmCrashUser = data.get("vmCrashUser")
        self.vmErrorNum = data.get("vmErrorNum")
        self.vmErrorUser = data.get("vmErrorUser")
        self.vmAccessNum = data.get("vmAccessNum")
        self.vmAccessUser = data.get("vmAccessUser")

class AdvancedSearchEx(BaseData):
    accessNum: int
    """联网次数"""
    accessUser: int
    """联网用户数"""
    appId: str
    """产品id"""
    crashNum: int
    """崩溃次数"""
    crashUser: int
    """崩溃用户数"""
    date: str
    """时间"""
    platformId: int
    """平台id"""
    version: str
    """项目版本"""

    def __init__(self, data):
        self.accessNum = data.get("accessNum")
        self.accessUser = data.get("accessUser")
        self.appId = data.get("appId")
        self.crashNum = data.get("crashNum")
        self.crashUser = data.get("crashUser")
        self.date = data.get("date")
        self.platformId = data.get("platformId")
        self.version = data.get("version")

class AppRealTimeTrendAppendEx(BaseData):
    accessNum: int
    """联网次数"""
    accessUser: int
    """联网用户数"""
    appId: str
    """产品id"""
    crashNum: int
    """崩溃次数"""
    crashUser: int
    """崩溃用户数"""
    date: str
    """时间"""
    platformId: int
    """平台id"""
    reportDeviceAllData: int
    reportNumAllData: int
    version: str
    """项目版本"""

    def __init__(self, data):
        self.accessNum = data.get("accessNum")
        self.accessUser = data.get("accessUser")
        self.appId = data.get("appId")
        self.crashNum = data.get("crashNum")
        self.crashUser = data.get("crashUser")
        self.date = data.get("date")
        self.platformId = data.get("platformId")
        self.reportDeviceAllData = data.get("reportDeviceAllData")
        self.reportNumAllData = data.get("reportNumAllData")
        self.version = data.get("version")

class IssueVersion(BaseData):
    """子issue版本"""
    count: int
    deviceCount: int
    firstUploadTime: str
    firstUploadTimestamp: int
    lastUploadTime: None
    lastUploadTimestamp: int
    version: str

    def __init__(self, data):
        self.count = data.get("count")
        self.deviceCount = data.get("deviceCount")
        self.firstUploadTime = data.get("firstUploadTime")
        self.firstUploadTimestamp = data.get("firstUploadTimestamp")
        self.lastUploadTime = data.get("lastUploadTime")
        self.lastUploadTimestamp = data.get("lastUploadTimestamp")
        self.version = data.get("version")

class TapdBug(BaseData):
    commercialTapd : bool
    bugPlatform : str
    id : str
    title : str
    workspaceId : str

    def __init__(self, data):
        self.commercialTapd = data.get("commercialTapd")
        self.bugPlatform = data.get("bugPlatform")
        self.id = data.get("id")
        self.title = data.get("title")
        self.workspaceId = data.get("workspaceId")

class Issue(BaseData):
    """issuse列表"""
    count: int
    """发生次数"""
    crashNum: int
    """崩溃次数"""
    exceptionMessage: str
    """异常消息"""
    exceptionName: str
    """异常名字"""
    ftName: str
    imeiCount: int
    """影响设备"""
    issueId: int
    """问题id"""
    issueVersions: List[IssueVersion]
    """子issue版本"""
    keyStack: str
    """堆栈信息"""
    lastestUploadTime: str
    """最近一次上报时间"""
    processor: str
    """issue处理人"""
    status: int
    """issue状态"""
    tagInfoList: str
    """标签信息列表"""
    version: str
    """项目版本"""
    bugs : List[TapdBug]
    """关联缺陷信息"""

    def __init__(self, data):
        self.count = data.get("count")
        self.crashNum = data.get("crashNum")
        self.exceptionMessage = data.get("exceptionMessage")
        self.exceptionName = data.get("exceptionName")
        self.ftName = data.get("ftName")
        self.imeiCount = data.get("imeiCount")
        self.issueId = data.get("issueId")
        self.issueVersions = [IssueVersion(issueVersion) for issueVersion in data.get("issueVersions")]
        self.keyStack = data.get("keyStack")
        self.lastestUploadTime = data.get("lastestUploadTime")
        self.processor = data.get("processor")
        self.status = data.get("status")
        self.tagInfoList = data.get("tagInfoList")
        self.version = data.get("version")
        self.bugs = [] if data.get("bugs") == None else [TapdBug(bug) for bug in data.get("bugs")]


class QueryIssueList(BaseData):
    appId: str
    """项目id"""
    issueList: List[Issue]
    """issuse列表"""
    numFound: int
    """崩溃总数"""
    platformId: str
    """平台id"""

    def __init__(self, data):
        self.appId = data.get("appId")
        self.issueList = [Issue(issue) for issue in data.get("issueList")]
        self.numFound = data.get("numFound")
        self.platformId = data.get("platformId")

class BugIssue(BaseData):
    """缺陷信息"""
    issueHash: str
    """问题hash"""
    title: str
    """标题"""
    description: str
    """描述"""
    reporter: str
    """创建人"""
    currentOwner: str
    """当前拥有者"""

    def __init__(self, issueHash : str, title : str, description : str, reporter : str, currentOwner : str):
        self.issueHash = issueHash
        self.title = title
        self.description = description
        self.reporter = reporter
        self.currentOwner = currentOwner
