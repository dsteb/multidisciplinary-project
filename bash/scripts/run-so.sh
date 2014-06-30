#!/bin/bash
pushd ~/mdp/mdp
    git pull
	i=$(uname -n | sed 's/[^0-9]//g')
    # hadoop1 hadoop2 hadoop3 => 1 2 3 
	i=$(($i + 39))
	nohup ./all.py $i > nohup.out 2> nohup.err < /dev/null &
popd
