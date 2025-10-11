#!/bin/bash

SHELL=/bin/sh
PATH=/sbin:/usr/sbin:/usr/bin:/bin

#for loss in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20;
for queue in 60 55 50 45 40 35 30 25 20 15 10 5;
do
	diretorio=Data
	BASEDIR=$(dirname $0)
	echo "Script location: ${BASEDIR}"
	if [ -e "$BASEDIR/$diretorio$queue" ]
	then
	echo " o diretorio existe"
	else
	echo " o diretorio não existe vamos criar o diretorio"
	mkdir /home/pedro/mn_iperf3/$diretorio$queue
	fi
	sudo python3 tcp_cc_mn_iperf4.py -a bbr bbr bbr2 bbr2 cubic cubic bic bic reno reno -d 10 -l 8 -q $queue
	mv *.txt $diretorio$queue
#	mv *.png $diretorio$loss
	

done
exit

#sudo python3 graf_bar.py
#exit
