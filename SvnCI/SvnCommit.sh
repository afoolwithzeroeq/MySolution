#!/usr/bin/env bash
export LANG=C.UTF-8

#参数判断  
if [ $# != 2 ];then  
    echo "Params error!"  
    echo "需要两个参数: 参数1.SVN提交路径 2.SVN提交记录信息"  
    exit 1
elif [ ! -d $1 ];then  
    echo "The first param is not a dictionary."  
    exit 1     
fi 

#Out路径
SVN_UP_PATH=$1
SVN_CI_MSG=$2

cd $SVN_UP_PATH

#export SVNPATH=/usr/local/bin/svn

svn cleanup

#$SVNPATH add . --no-ignore --force
svn status|grep ! |awk '{print $2}'|xargs svn del

svn add . --force

svn commit -m "$SVN_CI_MSG"

