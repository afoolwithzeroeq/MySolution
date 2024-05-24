#!/usr/bin/env bash
export LANG=C.UTF-8

#参数判断  
if [ $# != 1 ];then  
    echo "Params error!"  
    echo "需要两个参数: 参数1.SVN提交路径"  
    exit 1
elif [ ! -d $1 ];then  
    echo "The first param is not a dictionary."  
    exit 1     
fi 

#Out路径
SVN_CLEAN_UP_PATH=$1

cd $SVN_CLEAN_UP_PATH

svn cleanup
svn cleanup --remove-unversioned
svn cleanup --vacuum-pristines
svn revert -R ./
