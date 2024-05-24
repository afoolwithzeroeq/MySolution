#!/bin/bash
export LANG=C.UTF-8

#参数判断  
if [ $# != 2 ];then  
    echo "Params error!"  
    echo "需要两个参数: 参数1.本地svn目录 2.远程svnUrl"  
    exit 1
fi  

localPath=$1
svnUrl=$2

if [ -d "${localPath}" ];then
    cd ${localPath}
    StartVersion=`svnversion -c |sed 's/^.*://' |sed 's/[A-Z]*$//'`
    EndVersion=$(svn info ${svnUrl}| grep "Revision:" | awk -F ': ' '{print $2}')
    echo ${StartVersion}-${EndVersion}
else
    echo 0-0
fi