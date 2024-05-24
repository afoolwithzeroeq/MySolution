#!/usr/bin/env bash
export LANG=C.UTF-8

echo "start"

UNITY_PATH="xxx/Unity.app/Contents/MacOS/Unity"

UNITY_PROJECT_PATH="xxx"
#Log路径
LOG_FOLDER="xxx"
if [ ! -d $LOG_FOLDER ];then
    mkdir -p $LOG_FOLDER
fi

UNITY_LOG_PATH="${LOG_FOLDER}/xxx.txt"

Platform="Android"
#构建方法
BuildMethod="BuildCI.Build${Platform}Player"
#打包输出路径
UNITY_OUT_PATH="xxx"

echo "Start: BuildApk"
echo "UNITY_PATH:${UNITY_PATH}"
echo "UNITY_PROJECT_PATH:${UNITY_PROJECT_PATH}"
echo "UNITY_LOG_PATH:${UNITY_LOG_PATH}"
echo "BuildMethod:${BuildMethod}"
echo "UNITY_OUT_PATH:${UNITY_OUT_PATH}"
echo "BuildParms:${BuildParms}"

RedirectPath="${LOG_FOLDER}/xxx.txt"

{
    sh  -x ./UnityBatchCmd.sh "${UNITY_PATH}"  "${UNITY_PROJECT_PATH}" "${UNITY_LOG_PATH}" "${BuildMethod}" "${BuildParms}" "${Platform}" 1200 "${RedirectPath}"
}||{
    echo "Unity Error"
    unityResult=$(<${RedirectPath})
    failReason=""
    failDetails=""
    if echo "$unityResult" | grep -q "卡死超时"; then
        failReason="卡死超时"
        failDetails=`tail -n 10 ${UNITY_LOG_PATH}`
        failDetails="Unity卡死超过1200秒, 可手动重试。\n卡死日志: ${failDetails}"
    elif echo "$unityResult" | grep -q "threw exception"; then
        failReason="构建异常"
        {
            failDetails=`grep -n "threw exception" ${UNITY_LOG_PATH} | tail -n 1 | cut -d: -f1 | xargs -I {} awk 'NR < {} {if (/^[0-9]{4}-/) prev=""; if (prev != "") prev=prev "\n" $0; else prev=$0;} END {print prev}' ${UNITY_LOG_PATH}`
        }||{
            failDetails=`grep -B 10 "threw exception" ${UNITY_LOG_PATH}`
        }
        failDetails="构建异常, 检查构建逻辑。\n  异常详情:${failDetails}"
    elif echo "$unityResult" | grep -q "Unity Crash"; then
        failReason="UnityCrash"
        {
            failDetails=`grep -n "Native Crash Reporting" ${UNITY_LOG_PATH} | tail -n 1 | cut -d: -f1 | xargs -I {} awk 'NR < {} {if (/^[0-9]{4}-/) prev=""; if (prev != "") prev=prev "\n" $0; else prev=$0;} END {print prev}' ${UNITY_LOG_PATH}`
        }||{
            failDetails=`grep -B 10 "Native Crash Reporting" ${UNITY_LOG_PATH}`
        }
        failDetails="Unity崩溃, 可手动重试。\n  崩溃日志: ${failDetails}"
    elif echo "$unityResult" | grep -q "Scripts have compiler errors"; then
        failReason="编译错误"
        failDetails=`grep -m 1 "error CS" ${UNITY_LOG_PATH}`
        errorRegex="(.+)\((.+),(.+)\): error CS(.+)"
        # 匹配 Unity 编译错误行
        if [[ "$failDetails" =~ $errorRegex ]]; then
            filename=${BASH_REMATCH[1]}
            line=${BASH_REMATCH[2]}
            column=${BASH_REMATCH[3]}

            echo "File: $filename"
            echo "Line: $line"
            echo "Column: $column"

            cd "$UNITY_PROJECT_PATH" || exit 1
            svnInfo=$(svn blame "./${filename}" | awk "NR==${line}" | cut -d ' ' -f 1,2,3,4,5,6,7)
            IFS=' ' read -ra infoArray <<< "$svnInfo"
            svnVersion="${infoArray[0]}"
            svnAuthor="${infoArray[1]}"

            svnLog=$(svn log -r "$svnVersion" "./${filename}" | grep "-user=")

            failDetails="${failDetails}\n  提交版本: ${svnVersion}\n  提交人: ${svnAuthor} <@${svnAuthor}>\n  提交日志: ${svnLog}"
        fi
        failDetails="编译错误, 检查相关代码。\n  错误详情: ${failDetails}"
    else
        failReason="$unityResult"
    fi

    echo "${failReason}"
    echo "${failDetails}"
    exit 1
}
