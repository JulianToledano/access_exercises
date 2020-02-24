#!/bin/bash

typeset -A config # init config array
config=( # set default values in config array
    [destination]=""
    [source]=""
)

while getopts 'c:l:f' c
do
  case $c in
    c) configFile=$OPTARG ;;
    l) logFile=$OPTARG ;;
  esac
done
follow=0
for var in "$@"
do
    if test $var = '-f'
    then
        follow=1
    fi
done

# Checks files exist
if [ -z "$configFile" ]
then
    echo "[ERROR] Config file not initialized."
    exit 1
fi
if [ -z "$logFile" ]
then
    echo "[ERROR] Log file not initialized."
    exit 1
fi

if [ -f $logFile ]
then
    if test $follow -eq 1
    then
        echo "[INFO] Spawning log file reader process..."
        tail -n +1 -f input-file-10000.txt | python unlimited/load_data.py | tee -a logs/load_data.log &
    else
        echo "[INFO] Loading log file $logFile to Database."
        cat $logFile | python unlimited/load_data.py | tee -a logs/load_data.log
        echo "[INFO] Log file $logFile loaded."
fi
else
    echo "[ERROR] File not found."
    exit 1
fi


# Runs every hour
while :
do
    if [ -z "$configFile" ]
    then
        echo "[ERROR] File not initialized."
        exit 1
    else
        if test -f "$configFile"; 
        then
            while read line
            do
                if echo $line | grep -F = &>/dev/null
                then
                    varname=$(echo "$line" | cut -d '=' -f 1)
                    config[$varname]=$(echo "$line" | cut -d '=' -f 2-)
                fi
            done < $configFile
        else
            echo "[ERROR] File not found."
            exit 1
        fi
    fi    
    python unlimited/hourly.py ${config[destination]} ${config[source]} | tee -a logs/hourly.log
    if test $follow -eq 0
    then
        exit 1
    fi
    sleep 3600
done
