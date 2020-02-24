#!/bin/bash

# read the options
TEMP=`getopt -o f:h:b:e: --long file-name:,host:,beggining:,end: -- "$@"`
eval set -- "$TEMP"

# extract options and their arguments into variables.
while true ; do
    case "$1" in
        -f|--file-name)
            fileName=$2 ; shift 2 ;;
        -h|--host)
            host=$2 ; shift 2 ;;
        -b|--beggining)
            bts=$2 ; shift 2;;
        -e|--end)
            ets=$2 ; shift 2 ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac
done

# Check 
if [ -z "$fileName" ] || [ -z "$host" ] || [ -z "$bts" ] || [ -z "$ets" ]
then
    echo "[ERROR] Usage:"
    echo "       -f,--fileName [filename] -h,--host [hostname] -b,--beggining [starting timestamp] -e,--end [end timestamp]"
    echo "Example: ./exercise_one.sh --file-name input-file-10000.txt --host Cerena --beggining 1565647200000 --end 1565650800000"
else
    # Now take action
    cat $fileName | python parser/map.py $host | python parser/reduce.py $bts $ets
fi