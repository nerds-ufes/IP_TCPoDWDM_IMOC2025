#!/bin/bash -x

set -e

# For now, devices are all at the same IP address and port
#mn=localhost:8080; t1=$mn; t2=$mn
#for i in $(seq 1 n); do
#    echo "*t1 is at $t

echo "* t5 is at $t5"
echo "* t15 is at $t15"

# URL for REST server
url="localhost:8080"; #t1=$url; t2=$url; r1=$url; r2=$url

t5=$url; t15=$url; 

r1=$url; r2=$url
curl="curl -s"


echo "* Attempting to configure mult_link.py network"
$curl "$t5/connect?node=t5&ethPort=1&wdmPort=5&channel=5"
$curl "$t15/connect?node=t15&ethPort=1&wdmPort=15&channel=5"


echo "* Monitoring signals at endpoints"
$curl "$t5/monitor?monitor=t5-monitor"
$curl "$t15/monitor?monitor=t15-monitor"

echo "* Resetting ROADM"
$curl "$r1/reset?node=r1"
$curl "$r2/reset?node=r2"

echo "* Configuring ROADM to forward ch1 from t1 to t2"
$curl "$r1/connect?node=r1&port1=5&port2=25&channels=5"
$curl "$r2/connect?node=r2&port1=15&port2=25&channels=5"

###############################################

echo "* Turning on terminals/transceivers"
$curl "$t5/turn_on?node=t5"
$curl "$t15/turn_on?node=t15"

