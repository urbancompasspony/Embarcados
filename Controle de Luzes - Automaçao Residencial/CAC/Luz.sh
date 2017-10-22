#!/bin/bash

if [ $(pidof pcsc_scan) ]; then
       echo pcsc_scan is running
else
       pcsc_scan -n > ~/CAC/cardscan.txt &
fi

while inotifywait ~/CAC/cardscan.txt

do

tail -n 3 ~/CAC/cardscan.txt | grep "3B 79 18 00 00 42 72 61 7A 49 44 65 61 6C"

if [ $? == 0 ]; then
        echo unlocked
        python3 ~/Luzes/c4
		python3 ~/Luzes/lpli
else
        tail -n 3 ~/CAC/cardscan.txt | grep removed
        if [ $? == 0 ]; then
                python3 ~/Luzes/alldes
        fi
fi
done
