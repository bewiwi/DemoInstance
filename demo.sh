#!/bin/bash
[ -z "$PIDFILE" ] && PIDFILE="/var/run/demo_instance/demo.pid"
[ -z "$LOGFILE" ] && LOGFILE="/var/log/demo_instance.log"

cd $(dirname $0)
EXEC_START="python ./demo.py"

function is_up(){
    [ -f "$PIDFILE" ] || return 1
    ps aux | awk '{print $2}' | grep $(cat $PIDFILE)| grep -v grep 2>&1 1>/dev/null
    local RET=$?
    [[ $RET != "0" ]] && error "PID file exist and demo_instance is stopped"
    return $RET
}

function create_pid_folder(){
    mkdir -p $(dirname $PIDFILE)
    return $?
}

function error(){
    echo "ERROR : $@" >&2
    exit 1
}

case "$1" in
  start)
    create_pid_folder || error "Can't create pid folder"
    ($EXEC_START >> $LOGFILE 2>&1)&
    echo $! > $PIDFILE || error "Can't write pid file"
    sleep 1
    is_up && echo 'OK'
    ;;
  stop)
    kill $(cat $PIDFILE)
    rm "$PIDFILE"
    ;;
  status)
    is_up
    RET=$?
    [ $RET == "0" ] && echo "OK" || error "Stopped"
    exit $RET
    ;;
  *)
    echo "Usage: $0 {start|stop|status}"
esac
