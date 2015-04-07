#!/bin/bash
cd $(dirname $0)
. tools.sh

server_name=$1
server_name=${server_name:=nxserver_rob}

[ -z "`ps -ef|grep $server_name|grep -v grep`" ]&&echo -e "\t$server_name stop: \t\033[0m[\033[36m OK \033[0m]"&&exit
if [ "$2" = "force" ];then
    echo -e "\t$server_name stop: \t\033[0m[\033[36m OK \033[0m]"
    ps -ef|grep $server_name|grep -v grep |awk '{print $2}'|xargs kill -9
else
    ps -ef|grep $server_name|grep -v grep |awk '{print $2}'|xargs kill
fi

max_time=30
start_time=`date +%s`
while [ 1 ]
do
   if [ -z "`ps -ef|grep $server_name|grep -v grep`" ];then
        echo -e "\t$server_name stop: \t\033[0m[\033[36m OK \033[0m]"
        break
   fi
   sleep 3
   end_time=`date +%s`
   if [ "$[end_time-start_time]" -gt $max_time ];then
       echo -e "\t$server_name stop: \033[0m [\033[31m FAILED \033[0m]"
       break
   fi
done
log_file_fun "停服用时:$[end_time-start_time]秒"
