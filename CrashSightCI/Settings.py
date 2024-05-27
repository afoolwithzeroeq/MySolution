from Define import *

web_key = "xxxx" #企业微信机器人key

LocalUserId = {
    Channel.Global: "xxxx", #CrashSight用户ID
    Channel.China: "xxxx"
}

UserOpenapiKey = {
    Channel.Global: "xxxx", #CrashSight用户OpenAPIKey
    Channel.China: "xxxx"
}

RequestUrl = {
    Channel.Global: 'https://crashsight.wetest.net/uniform/openapi/',
    Channel.China: 'https://crashsight.qq.com/uniform/openapi/'
}

PlatformId = {
    Platform.Android: 1,
    Platform.iOS: 2,
    # Platform.PC: 10
}

AppId = {
    Channel.Global: {
        Platform.Android: "xxxx", #CrashSight应用ID
        Platform.iOS: "xxxx"
    },
    Channel.China: {
        Platform.Android: "xxxx",
        Platform.iOS: "None"
    }
}

# open_all 地区国家列表(仅全球渠道)
OpenAllCountries = [
    "加拿大",
    "菲律宾",
    "新加坡",
    "墨西哥",
    "西班牙",
    "新西兰",
    "澳大利亚",
    "美国",
    "德国",
    "英国",
    "法国",
]

# 关注版本列表
VersionList = [
    Version(Channel.Global, Platform.Android, "0.6.13547.798"),
    Version(Channel.Global, Platform.iOS, "0.6.13544.481"),
    # Version(Channel.China, Platform.Android, "0.6.13665.107"),
]

# 值班人列表
DutyGroup = {
    1: ["xxxx", "xxxx"], # 企业微信用户名, 邮箱前缀
    # 4: [""],
}
# 当前值班人
DutyMan = DutyGroup[1]