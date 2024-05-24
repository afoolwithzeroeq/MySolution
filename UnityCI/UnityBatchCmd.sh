#!/usr/bin/env bash
export LANG=C.UTF-8

#参数判断  
if [ $# -lt 5 ];then  
    echo "Params error!"  
    echo "需要至少五个参数: 参数1.Unity路径 2.工程路径 3.打包Log路径 4.构建函数名 5.构建参数 6.目标平台(可选) 7.卡住超时时间/s(可选) 8.重定向路径(可选)"  
    exit 1
fi  

#Unity.app或Unity.exe的路径
UNITY_PATH=$1
#项目路径
UNITY_PROJECT_PATH=$2
#Log路径
UNITY_LOG_PATH=$3
#构建函数名
BuildMethod=$4
#构建参数
BuildParms=$5
#目标平台(Android, iOS, StandaloneWindows64)
BuildTarget=$6
#卡住超时时间, 超过这个时间会kill掉Unity进程, Windows下无效
MaxTimeStamp=$7
#重定向路径
RedirectPath=$8

if [ "${MaxTimeStamp}"x != ""x ]; then
	echo "unity will be killed if log stagnated more than ${MaxTimeStamp} seconds!"
fi

BuildParms=`echo $BuildParms | sed 's/\"//g'`

execute_logic() {
	if [ "${BuildTarget}"x != ""x ]; then
		$UNITY_PATH -quit -batchmode -timestamps -silent-crashes -buildTarget "${BuildTarget}" -projectPath $UNITY_PROJECT_PATH -logFile $UNITY_LOG_PATH -executeMethod ${BuildMethod} "${BuildParms}"
	else
		$UNITY_PATH -quit -batchmode -timestamps -silent-crashes -projectPath $UNITY_PROJECT_PATH -logFile $UNITY_LOG_PATH -executeMethod ${BuildMethod} "${BuildParms}"
	fi
}

if [ "${CurSys}" != "Darwin" ]; then
	execute_logic && {
		cat $UNITY_LOG_PATH
		echo "build success"
		exit 0
	} || {
		cat $UNITY_LOG_PATH
		echo "build failed"
		exit 1
	}
else
	pid=$(ps -ef | grep ${UNITY_PROJECT_PATH} | grep Unity | grep -v "sh -x" | head -1 | awk -F" " '{print $2}')
	echo ${pid} ${UNITY_PROJECT_PATH}

	start_time=$(date +"%s")
	while true; do
		# 检查后台任务是否还在运行
		cur_time=$(date +"%s")
		echo "cur timestamps: $cur_time"
		if [ "${pid}"x == ""x ];then
			break
		fi
		if ps -p $pid > /dev/null; then
			kill -9 $pid
			sleep 6
		else
			break
		fi
	done
	
	if [ ${RedirectPath}x == ""x ]; then
		RedirectPath="unity_result.txt"
	fi

	execute_logic > ${RedirectPath} &

	#UnityPid=$!
	# sleep 10

	check_interval=10

	start_time=$(date +"%s")
	while true; do
		UnityPid=$(ps -ef | grep ${UNITY_PROJECT_PATH} | grep Unity | grep -v "sh -x" | head -1 | awk -F" " '{print $2}')
		echo "UnityPid" ${UnityPid}
		if [ "${UnityPid}"x != ""x ]; then
			break
		fi

		cur_time=$(date +"%s")
		if [ $((cur_time - start_time)) -gt 60 ]; then
			if [ -e $RedirectPath ];then
				cat $RedirectPath
				exit 1
			else
				echo "Unity启动失败" > ${RedirectPath}
				exit 1
			fi
		fi

		sleep 5
	done

	max_change_time=0
	last_line_count=0
	last_time=0

	# 定时检测后台任务的执行状态
	while true; do
	  # 检查后台任务是否还在运行
	  cur_time=$(date +"%s")
	  echo "cur timestamps: $cur_time"
	  if ps -p $UnityPid > /dev/null; then
		# 后台任务仍在运行，继续等待
		if [ -e $UNITY_LOG_PATH ];then
			cur_line_count=$(wc -l < $UNITY_LOG_PATH)
			if [ $last_line_count -eq 0 ];then
				echo "unity log exist"
				last_line_count=$cur_line_count
				last_time=$cur_time
			elif [ $last_line_count -eq $cur_line_count ];then
				echo "unity log not change"
				if [ "${MaxTimeStamp}"x != ""x ]; then
					cur_dur_time=`expr $cur_time - $last_time`
					if [ $cur_dur_time -ge $MaxTimeStamp ];then
						{
							dir_name=$(dirname $UNITY_LOG_PATH)
							file_name=$(basename $UNITY_LOG_PATH)
							pstreeFile="${dir_name}/pstree_${file_name}"
							pstree -p $UnityPid > $pstreeFile
							# pstree信息可自行处理
						}&&{
							echo "try kill $UnityPid"
							kill -9 $UnityPid
							echo "unity stagnated more than $MaxTimeStamp seconds, killed"
							exit 1
						}
					fi
				fi
			else
				echo "unity log changed"
				last_line_count=$cur_line_count
				cur_change_time=`expr $cur_time - $last_time`
				last_time=$cur_time
				if [ $cur_change_time -ge $max_change_time ];then
					max_change_time=$cur_change_time
				fi
				echo "cur: ${cur_change_time} max: ${max_change_time}"
			fi
		else
			echo "unity log file not exist"
		fi
		
	  else
		# 后台任务已结束，停止定时检测
		echo "unity execution completed."
		break
	  fi
	  sleep $check_interval
	done

	result=$(<${RedirectPath})
	echo "$result"
	echo "max_change_time:${max_change_time}"
	if [ "$result"x == ""x ];then
		cat $UNITY_LOG_PATH
		#在log文件中查找Crash信息
		if [ -e $UNITY_LOG_PATH ];then
			if grep -q "Native Crash Reporting" $UNITY_LOG_PATH;then
				echo "Unity Crash" > ${RedirectPath}
				echo "Unity Crash"
				exit 1
			elif ! grep -q "${BuildMethod}" $UNITY_LOG_PATH;then
				echo "Unity未正常启动" > ${RedirectPath}
				echo "Unity未正常启动"
				exit 1
			fi
		fi

		echo "build success"
	else
		cat $UNITY_LOG_PATH
		sleep 10
		echo "build failed"
		echo "$result"
		exit 1
	fi
fi

