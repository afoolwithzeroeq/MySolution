#!/usr/bin/env bash
 
#参数判断  
if [ $# != 4 ];then  
    echo "Params error!"  
    echo "Need four params: 1.path of project 2.path of output 3.name of ipa file 4.name of app"  
    exit 1
elif [ ! -d $1 ];then  
    echo "The first param is not a dictionary."  
    exit 1     
elif [ ! -d $2 ];then  
    echo "The second param is not a dictionary."  
    exit 1
fi  
#工程路径  
project_path=$1  
echo "工程路径"${project_path}
 
#输出路径
outputPath=$2

#IPA名称  
ipa_name=$3

#APP名称
app_name=$4

#XCode默认导出名称
app_name_nospace=`echo "${app_name}" | sed 's/ //g' | sed 's/&//g'` 

echo "$app_name_nospace"

#编译工程  
cd $project_path  

build_temp_path=${ipa_name%%.*}

xcodebuild -exportArchive -archivePath build/${build_temp_path}-adhoc.xcarchive -exportPath build/${build_temp_path} -allowProvisioningUpdates #"CODE_SIGN_IDENTITY"="${code_sign}" -exportOptionsPlist ExportOptions.plist

cd build/${build_temp_path}
ipaFileName=`ls |grep .ipa`

if [ ! -f $ipaFileName ];then  
    echo "没有找到IPA文件"  
    exit 1
else
    cp $ipaFileName ${outputPath}/${ipa_name}
fi  

exit  
 
