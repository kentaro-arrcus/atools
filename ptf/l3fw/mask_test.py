"""
Experimental test to test Packet Field Masking
"""
import ptf
from ptf.testutils import *

import base_test


class MaskTest(base_test.DutTest):
    def runTest(self):
        print("Running:", self.__class__.__name__)

        # $PTF --test-dir ./ --interface 0@veth11 --interface 1@veth21
        port1 = 0
        port2 = 1
        
        mac_veth10 = "02:03:04:05:06:10"
        mac_veth11 = "02:03:04:05:06:11"
        mac_veth20 = "02:03:04:05:06:20"
        mac_veth21 = "02:03:04:05:06:21"
        ipv4_veth10 = "10.0.10.10"
        ipv4_veth11 = "10.0.10.1"
        ipv4_veth20 = "10.0.20.10"
        ipv4_veth21 = "10.0.20.1"

        # ptf/src/testutils.py
        pkt1 = simple_ip_packet(
            pktlen  = 110,
            eth_src = mac_veth11,  eth_dst = mac_veth10,
            ip_src  = ipv4_veth11, ip_dst  = ipv4_veth21,
            ip_ttl  = 64,
        )

        pkt2 = simple_ip_packet(
            pktlen  = 110,
            eth_src = mac_veth20,  eth_dst = mac_veth21,
            ip_src  = ipv4_veth11, ip_dst  = ipv4_veth21,
            ip_ttl  = 64, # TTL is 63 in the receiving packet.
        )
        m = ptf.mask.Mask(pkt2)
        m.set_do_not_care_scapy(IP, 'ttl')
        m.set_do_not_care_scapy(IP, 'chksum')

        try:
            ## def send_packet(test, port_id, pkt, count=1)
            send_packet(self, 0, pkt1)
            #verify_packets(self, pkt2, ports=[1])
            verify_packets(self, m, ports=[1])
        finally:
            pass

