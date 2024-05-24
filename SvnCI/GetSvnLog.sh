#!/bin/bash
if [ ! "${CurSys}" == "MINGW64_NT-10.0-22000" ]; then
    export LANG=C.UTF-8
fi
 
#参数判断
if [ $# != 3 ];then  
    echo "Params error!"  
    echo "需要两个参数: 参数1.Svn开始版本 2.Svn结束版本 3.日志存放文件"  
    exit 1
fi

StartVersion=$1
EndVersion=$2
LogFile=$3

if [ $EndVersion -le $StartVersion ]; then
    echo " " >${LogFile}
else
    echo "版本号:${StartVersion}--${EndVersion}"  >${LogFile}
    svn log -r r${StartVersion}:r${EndVersion} >>${LogFile}
fi