#!/bin/bash
find_parents (){
    local parents=$(pgrep -P $1)
    echo "$parents"
}

get_process_name(){
    echo $(ps -p $1 -o comm --no-headers)
}

print_proc_tree(){
    processes=$(find_parents $1 | tr " " "\n") 
    for proc in $processes
    do
        get_process_name $proc
        print_proc_tree $proc
    done
}

pid=$1
print_proc_tree $pid
