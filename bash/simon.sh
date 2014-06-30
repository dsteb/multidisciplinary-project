#!/bin/bash

# run input script on each hadoop cluster


if [ "$1" == "put" ]; then
	echo "Simon says run this command '$2'"
	for i in `seq 2 10`; do
		scp $2 azureuser@hadoop$i:~/mdp/$2
		ssh azureuser@hadoop$i "bash ~/mdp/$2"
		echo -e "\e[1;32m server $i DONE \e[0;37m"
	done 
else
	echo "Simon says run this command '$1'"
	for i in `seq 2 10`; do
		ssh azureuser@hadoop$i $1
		echo -e "\e[1;32m server $i DONE \e[0;37m"
	done 
fi

