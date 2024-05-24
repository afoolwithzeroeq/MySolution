#!/usr/bin/env bash
export LANG=C.UTF-8

#参数判断  
if [ $# -le 1 ];then  
    echo "Params error!"  
    echo "需要至少3个参数: 参数1.Svn检出路径 2.SvnUrl 3.revision(0表示到最新版本) (非必须)4~... 还原路径"  
    exit 1
fi

echo "svn up"
SVN_CHECKOUT_PATH=$1
SVN_CHECKOUT_URL=$2
REVISION=$3

CurDir=$(pwd)
CurSys=`uname`

index=0
for i in $*        #在$*中遍历参数，此时每个参数都是独立的，会遍历$#次
do
    let index+=1
    if [ $index -gt 2 ];then
        echo $i
        if [ -d ${i} ];then
            cd ${i}
            svn cleanup --remove-unversioned
            svn revert -R ./
            cd ${CurDir}
        fi
    fi
done

cd ${SVN_CHECKOUT_PATH}
cd ${SVN_CHECKOUT_URL##*/}

svn cleanup --vacuum-pristines

cd ${SVN_CHECKOUT_PATH}

echo "${CurSys}"
if [ "${CurSys}" == "Linux" ];then
	if [ "${REVISION}"x == "0"x ];then
		svn checkout ${SVN_CHECKOUT_URL} --non-interactive
	else
		svn checkout -r ${REVISION} ${SVN_CHECKOUT_URL} --non-interactive
	fi
else
	if [ "${REVISION}"x == "0"x ];then
		svn checkout ${SVN_CHECKOUT_URL} --non-interactive --trust-server-cert-failures="unknown-ca,cn-mismatch,expired,not-yet-valid,other"
	else
        # # 先判断本地是否存在，如果存在，使用svn update
        # if [ -d ${SVN_CHECKOUT_PATH}/${SVN_CHECKOUT_URL##*/} ];then
        #     cd ${SVN_CHECKOUT_PATH}/${SVN_CHECKOUT_URL##*/}
        #     svn cleanup --vacuum-pristines
        #     svn revert -R ./
        #     svn update -r ${REVISION} --non-interactive --trust-server-cert-failures="unknown-ca,cn-mismatch,expired,not-yet-valid,other"
        # else
            svn checkout -r ${REVISION} ${SVN_CHECKOUT_URL} --non-interactive --trust-server-cert-failures="unknown-ca,cn-mismatch,expired,not-yet-valid,other"
        # fi
	fi
fi
