#!/bin/bash
cd $(dirname $0)

server_name=$1
server_name=${server_name:=nxserver_rob Lcj}
log_dir_root=/data/logs/gunsoul_mobile_rob
log_dir_cur=$log_dir_root/`date +%Y_%m_%d`

[ ! -z "`ps -ef|grep "$server_name"|grep -v grep`" ]&&echo $server_name is runing&& exit
echo "core-%e-%p-%t" > /proc/sys/kernel/core_pattern
ulimit -c unlimited
if [ -d "Lua" ]; then
        script_dir="Lua"
elif [ -d "Lcj" ]; then
        script_dir="Lcj"
else
        echo -e "\033[41;37mstart server script directory not exist\033[0m"
                exit 0
fi
nohup ./nxserver_rob $script_dir main $log_dir_root NXServer_rob >/dev/null 2>&1 &
rm -rf Log
ln -s $log_dir_cur ./Log
#env HEAPCHECK=normal PPROF_PATH=/usr/local/bin/pprof ./nxserver_rob
#valgrind --tool=memcheck --leak-check=full --track-fds=yes ./nxserver_rob

if [  -z "`ps -ef|grep "$server_name"|grep -v grep`" ];then
    echo -e "\tnxserver_rob start: \033[0m [\033[31m FAILED \033[0m]"
else
    echo -e "\tnxserver_rob start: \t\033[0m[\033[36m OK \033[0m]"
fi
