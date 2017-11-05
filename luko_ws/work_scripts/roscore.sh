#!/bin/bash

TIMESTAMP=(`date +%y%m%d_%H%M%S`)
LOG_DIR=$ROS_BASE_DIR/work_scripts/logs
PID_FILE=$LOG_DIR/.roscore
LOG_FILE=$LOG_DIR/roscore.log



start_ros () {
	if [ -f $LOG_FILE ]; then
		echo "roscore already running on $(cat $PID_FILE)"
	else 
		echo "starting roscore"
		echo $TIMESTAMP > $LOG_FILE
		stdbuf -oL -eL roscore >> $LOG_FILE 2>&1 &
		echo $! > $PID_FILE
		echo "[$!]"
	fi
}

stop_ros () {
    if [ -f $PID_FILE ]; then
		PID=(`cat $PID_FILE`)
		TS=(`head -1 $LOG_FILE`)	
		echo "Killing $PID"
		kill $PID
		rm $PID_FILE
		mv $LOG_FILE $LOG_DIR/roscore_$TS.log
	else 
		echo "cannot find running ros"
	fi
}



if [ "$1" == "start" ]; then
    start_ros
elif [ "$1" == "stop" ]; then
    stop_ros
elif [ "$1" == "restart" ]; then
    stop_ros
    start_ros
else
	echo "Argument needed:"
	echo "  start"
	echo "  stop"
fi

#stdbuf -oL -eL roscore > $LOG_DIR/roscore_$TIMESTAMP.log 2>&1 &

#echo $! > $LOG_DIR/.ros_pid.tmp
