#!/usr/bin/env python3

"""
mult_link.py: simple link between terminals & switches
h1 --- t1 -- r1 -- r2 -- t2 --- h2
hn --- tn _/          \_ tn --- hn
Use ./config-multi_link.sh
This is very close to the simplest fully emulated packet-optical
network that we can create.

"""
from time import sleep, mktime
import csv
from datetime import datetime
import matplotlib
matplotlib.use('Agg')   # Force matplotlib to not use any Xwindows backend.
import matplotlib.pyplot as plt

from mnoptical.dataplane import (
    OpticalLink, UnidirectionalOpticalLink as ULink,
    ROADM, Terminal, OpticalNet as Mininet, km, m, dB, dBm )
from mnoptical.node import Amplifier
from mnoptical.ofcdemo.demolib import OpticalCLI as CLI, cleanup

from mnoptical.rest import RestServer
from mnoptical.ofcdemo.demolib import OpticalCLI as CLI

from mininet.node import OVSBridge, Host
from mininet.topo import Topo

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections, quietRun
from mininet.log import info, lg, setLogLevel
from mininet.log import setLogLevel, info
from mininet.clean import cleanup

from os.path import dirname, realpath, join
from subprocess import run
from sys import argv
import argparse
import os
import subprocess


import sys
import time
import threading
import socket
import numpy as np

#########################################################################
################ DELETA AS INFERFACES CRIADAS ###########################
#########################################################################
def limpa_int():
	os.system("sudo mn -c")
	interfaces = ["r1-wdm5","r1-wdm25","r2-wdm15","r2-wdm25","s1-eth1","s1-eth2","s2-eth1","s2-eth2","s3-eth1","s4-eth1","t5-wdm5","t15-wdm15","h101-eth0","t5-eth1","h102-eth0","t15-eth1"]
	for interface in interfaces:
		subprocess.run(["sudo","ip","link","delete", interface])

#################################################################
#################### DEFINIÇÃO DA REDE  ######################### 
#################################################################

class SimpleLinkTopo(Topo):
    """Simple link topology:
       h1 - t1 - (boost->) --25km-- (<-boost) - t2 - h2"""

    def build(self, delay=2, loss = 0, queue = 100):

        # The bandwidth (bw) is in Mbps, delay in milliseconds and queue size is in packets
        #br_params = dict(bw=200, delay='{0}ms'.format(delay[0]), max_queue_size=30*v_delay[0], use_htb=True)  # backbone router interface tc params
        #br_params = dict(bw=200, delay='{0}ms'.format(delay[0]), max_queue_size=8.33*(queue/100)*v_delay[0], use_htb=True)
        br_params = dict(bw=100, delay='{0}ms'.format(delay[0]), max_queue_size=8.33*(queue/100)*1*v_delay[0], use_htb=True)  
        ar_params = dict(bw=100, delay='0ms', max_queue_size=(21*v_delay[0]*20)/100, use_htb=True)  # access router intf tc params
        #ar_params = dict(bw=100, delay='0ms', max_queue_size= 0, use_htb=True)  # access router intf tc params
        # TODO: remove queue size from hosts and try.
        hi_params = dict(bw=100, delay='0ms', max_queue_size=100*v_delay[0], use_htb=True)  # host interface
        #hi_params = dict(bw=100, delay='0ms', max_queue_size= 0, use_htb=True)  # host interface 

        """ Create the topology by overriding the class parent's method.

            :param  delay   One way propagation delay, delay = RTT / 2. Default is 2ms.
            Obs: 
        """
                
        # Create routers s1 to s4
        s1 = self.addSwitch('s1', failMode='standalone', stp=True)
        s2 = self.addSwitch('s2', failMode='standalone', stp=True)
        s3 = self.addSwitch('s3', failMode='standalone', stp=True)
        s4 = self.addSwitch('s4', failMode='standalone', stp=True)

# Link backbone routers (s1 & s2) together
# self.addLink(s1, s2, cls=TCLink, **br_params)
        # Ethernet links
        self.addLink(s1,t1)
        self.addLink(s2,t2)
        
# WDM link
        boost = ('boost', {'target_gain': 3.0*dB})
        # amp1 = ('amp1', {'target_gain': 25*.22*dB})
        # amp2 = ('amp2', {'target_gain': 40*.22*dB})
        # amp3 = ('amp3', {'target_gain': 50*.22*dB})
        # spans = [5*km, amp1, 5*km, amp2]
        spans = [50*km]

        # Link backbone routers (s1 & s2) together
        #self.addLink(s1, s2, cls=TCLink, **br_params)

        # Link access routers (s3 & s4) to the backbone routers
        #self.addLink(s1, s3, cls=TCLink, **ar_params)
        #self.addLink(s2, s4, cls=TCLink, **ar_params)

        # Create the hosts h1x to h2x, and link them to access router 1
        
        h10 = self.addHost('h10',ip='10.0.0.10')
        h11 = self.addHost('h11',ip='10.0.0.11')
        h12 = self.addHost('h12',ip='10.0.0.12')
        h13 = self.addHost('h13',ip='10.0.0.13')
        h14 = self.addHost('h14',ip='10.0.0.14')
        h15 = self.addHost('h15',ip='10.0.0.15')
        h16 = self.addHost('h16',ip='10.0.0.16')
        h17 = self.addHost('h17',ip='10.0.0.17')
        h18 = self.addHost('h18',ip='10.0.0.18')
        h19 = self.addHost('h19',ip='10.0.0.19')
        
        h20 = self.addHost('h20',ip='10.0.0.20')
        h21 = self.addHost('h21',ip='10.0.0.21')
        h22 = self.addHost('h22',ip='10.0.0.22')
        h23 = self.addHost('h23',ip='10.0.0.23')
        h24 = self.addHost('h24',ip='10.0.0.24')
        h25 = self.addHost('h25',ip='10.0.0.25')
        h26 = self.addHost('h26',ip='10.0.0.26')
        h27 = self.addHost('h27',ip='10.0.0.27')
        h28 = self.addHost('h28',ip='10.0.0.28')
        h29 = self.addHost('h29',ip='10.0.0.29')
        
        

        # Link the source hosts (h1 & h3) to access router 1 (s3)
        self.addLink(s3, h10, cls=TCLink, **hi_params)
        self.addLink(s3, h11, cls=TCLink, **hi_params)
        self.addLink(s3, h12, cls=TCLink, **hi_params)
        self.addLink(s3, h13, cls=TCLink, **hi_params)
        self.addLink(s3, h14, cls=TCLink, **hi_params)
        self.addLink(s3, h15, cls=TCLink, **hi_params)
        self.addLink(s3, h16, cls=TCLink, **hi_params)
        self.addLink(s3, h17, cls=TCLink, **hi_params)   
        self.addLink(s3, h18, cls=TCLink, **hi_params)
        self.addLink(s3, h19, cls=TCLink, **hi_params)
   

        # Link the receiver hosts (h2 & h4) to access router 2 (s4)
        self.addLink(s4, h20, cls=TCLink, **hi_params)
        self.addLink(s4, h21, cls=TCLink, **hi_params)
        self.addLink(s4, h22, cls=TCLink, **hi_params)
        self.addLink(s4, h23, cls=TCLink, **hi_params)
        self.addLink(s4, h24, cls=TCLink, **hi_params)
        self.addLink(s4, h25, cls=TCLink, **hi_params)
        self.addLink(s4, h26, cls=TCLink, **hi_params)
        self.addLink(s4, h27, cls=TCLink, **hi_params)
        self.addLink(s4, h28, cls=TCLink, **hi_params)
        self.addLink(s4, h29, cls=TCLink, **hi_params)
        
        
        self.addLink( 's3','s1' , cls=TCLink, **ar_params )
        self.addLink( 's4','s2' , cls=TCLink, **ar_params )
        self.addLink( 's1','s2' , cls=TCLink, loss = (v_loss[0])/10, **br_params )

topos = {'mytopo': (lambda: SimpleLinkTopo())}


def tcp_test(algs, delays, p_loss, queue):

    limpa_int()
    global v_loss
    global v_delay
    global v_queue
    v_loss = p_loss
    v_delay = delays
    v_queue = float(queue[0])
    
    topo = SimpleLinkTopo(delay=v_delay,loss=v_loss, queue = v_queue)
    net = Mininet(topo=topo, switch=OVSBridge,controller=None)
    h10, h11, h12, h13, h14, h15, h16, h17, h18, h19 = net.get('h10','h11','h12','h13','h14','h15','h16','h17','h18','h19')
    h20, h21, h22, h23, h24, h25, h26, h27, h28, h29 = net.get('h20','h21','h22','h23','h24','h25','h26','h27','h28','h29')
    host_addrs = dict({'h10': h10.IP(), 'h11': h11.IP(), 'h12': h12.IP(), 'h13': h13.IP(), 'h14': h14.IP(), 'h15': h15.IP(),'h16': h16.IP(), 'h17': h17.IP(), 'h18': h18.IP(),'h19': h19.IP(), 'h20': h20.IP(), 'h21': h21.IP(), 'h22': h22.IP(),'h23': h23.IP(), 'h24': h24.IP(), 'h25': h25.IP(), 'h26': h26.IP(), 'h27': h27.IP(), 'h28': h28.IP(), 'h29': h29.IP()})
    print('Host addrs: {0}'.format(host_addrs))
    
    #net = Mininet(topo)
    net.start()
    net.pingAll()

    popens = dict()
    
    alg_ajustado = set(algs)
    for a in alg_ajustado:
        print("*** Starting teste de capacidade de canal para  ...")
        print("*** Starting iperf alg {}...".format(a))
        popens[h20] = h20.popen(['iperf3', '-s', '-p', '5001'])
        delay = v_delay[0]

        runtime = 50
        popens[h10] = h10.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -Z {1} -t {2} >> iperf_taxa_max_{1}_{3}ms.txt'.format(h20.IP(), a, runtime, delay), shell=True)
        popens[h10].wait()
        popens[h20].terminate()
        popens[h20].wait()
 
    
    print("*** Starting iperf servers ...")
    popens[h20] = h20.popen(['iperf3', '-s', '-p', '5001'])
    popens[h21] = h21.popen(['iperf3', '-s', '-p', '5001'])
    popens[h22] = h22.popen(['iperf3', '-s', '-p', '5001'])
    popens[h23] = h23.popen(['iperf3', '-s', '-p', '5001'])
    popens[h24] = h24.popen(['iperf3', '-s', '-p', '5001'])
    popens[h25] = h25.popen(['iperf3', '-s', '-p', '5001'])
    popens[h26] = h26.popen(['iperf3', '-s', '-p', '5001'])
    popens[h27] = h27.popen(['iperf3', '-s', '-p', '5001'])
    popens[h28] = h28.popen(['iperf3', '-s', '-p', '5001'])
    popens[h29] = h29.popen(['iperf3', '-s', '-p', '5001'])
    
    
    #delay = delays
    delay = v_delay[0]
    iperf_runtime = 200
    #alg = ['cubic','cubic','cubic','cubic','cubic','cubic','cubic','cubic','cubic','cubic']
    alg = algs
    print("*** Starting iperf client h1...")
    popens[h10] = h10.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -C {1} -t {2} >> iperf_{1}_{3}-{4}_{5}ms.txt'.format(h20.IP(), alg[0], iperf_runtime, 'h10', 'h20', delay), shell=True)
    popens[h11] = h11.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -C {1} -t {2} >> iperf_{1}_{3}-{4}_{5}ms.txt'.format(h21.IP(), alg[1], iperf_runtime, 'h11', 'h21', delay), shell=True)
    popens[h12] = h12.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -C {1} -t {2} >> iperf_{1}_{3}-{4}_{5}ms.txt'.format(h22.IP(), alg[2], iperf_runtime, 'h12', 'h22', delay), shell=True)
    popens[h13] = h13.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -C {1} -t {2} >> iperf_{1}_{3}-{4}_{5}ms.txt'.format(h23.IP(), alg[3], iperf_runtime, 'h13', 'h23', delay), shell=True)
    popens[h14] = h14.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -C {1} -t {2} >> iperf_{1}_{3}-{4}_{5}ms.txt'.format(h24.IP(), alg[4], iperf_runtime, 'h14', 'h24', delay), shell=True)
    popens[h15] = h15.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -C {1} -t {2} >> iperf_{1}_{3}-{4}_{5}ms.txt'.format(h25.IP(), alg[5], iperf_runtime, 'h15', 'h25', delay), shell=True)
    popens[h16] = h16.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -C {1} -t {2} >> iperf_{1}_{3}-{4}_{5}ms.txt'.format(h26.IP(), alg[6], iperf_runtime, 'h16', 'h26', delay), shell=True)
    popens[h17] = h17.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -C {1} -t {2} >> iperf_{1}_{3}-{4}_{5}ms.txt'.format(h27.IP(), alg[7], iperf_runtime, 'h17', 'h27', delay), shell=True)
    popens[h18] = h18.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -C {1} -t {2} >> iperf_{1}_{3}-{4}_{5}ms.txt'.format(h28.IP(), alg[8], iperf_runtime, 'h18', 'h28', delay), shell=True)
    popens[h19] = h19.popen('iperf3 -c {0} -p 5001 -i 1 -w 16m -M 1460 -N -C {1} -t {2} >> iperf_{1}_{3}-{4}_{5}ms.txt'.format(h29.IP(), alg[9], iperf_runtime, 'h19', 'h29', delay), shell=True)
    
    print("*** Waiting {0}sec for iperf clients to finish...".format(iperf_runtime))
    popens[h10].wait()
    popens[h11].wait()
    popens[h12].wait()
    popens[h13].wait()
    popens[h14].wait()
    popens[h15].wait()
    popens[h16].wait()
    popens[h17].wait()
    popens[h18].wait()
    popens[h19].wait()
    
    # Terminate the servers and tcpprobe subprocesses
    print('*** Terminate the iperf servers and tcpprobe processes...')
    popens[h20].terminate()
    popens[h21].terminate()
    popens[h22].terminate()
    popens[h23].terminate()
    popens[h24].terminate()
    popens[h25].terminate()
    popens[h26].terminate()
    popens[h27].terminate()
    popens[h28].terminate()
    popens[h29].terminate()
    
    popens[h20].wait()
    popens[h21].wait()
    popens[h22].wait()
    popens[h23].wait()
    popens[h24].wait()
    popens[h25].wait()
    popens[h26].wait()
    popens[h27].wait()
    popens[h28].wait()
    popens[h29].wait()
    
    print("*** Stopping test...")
    
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    parser = argparse.ArgumentParser(description='TCP Congestion Control tests in a dumbbell topology.')
    parser.add_argument('-a', '--algorithms', nargs='+', default=['cubic','cubic','cubic','cubic','cubic','cubic','cubic','cubic','cubic','cubic'], help='List TCP Congestion Control algorithms to test.')
    parser.add_argument('-d', '--delays', nargs='+', type=int, default= 10, help='List of backbone router one-way propagation delays to test.')
    parser.add_argument('-l', '--loss', nargs='+' , type=int, default= 0 , help='Verbosity level of the logger. Uses `info` by default.')
    parser.add_argument('-q', '--queue', nargs='+' , type=int, default= 100 , help='Verbosity level of the logger. Uses `info` by default.')
    args = parser.parse_args()
    
    tcp_test(args.algorithms, args.delays, args.loss, args.queue)

