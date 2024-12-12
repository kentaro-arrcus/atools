"""
L3 IPv4 forwarding TTL test. Expect TTL expired.
"""
import ptf
from ptf.testutils import *
import ptf.packet as p #scapy

import base_test

# TODO: Add class to connect to and configure DUT(switch)

class L3Ipv4(base_test.DutTest):
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

        pkt1 = p.Ether(
            src = mac_veth11,
            dst = mac_veth10,
        )
        pkt1 /= p.IP(
            ttl = 1,
            proto = 0,
            src = ipv4_veth11,
            dst = ipv4_veth21,
        )

        pkt2 = p.Ether(
            src = mac_veth10,
            dst = mac_veth11,
        )
        pkt2 /= p.IP(
            ihl = 5,
            tos = 192,
            len = 48,
            #id = 9140, #ignore
            ttl = 64,
            #chksum = xx, #ignore
            src = ipv4_veth10,
            dst = ipv4_veth11,
        )
        pkt2 /= p.ICMP(
            type = 11, #Time Exceeded
            #chksum = 62719, #ignore
        )
        pkt2 /= p.IP(
            ihl = 5,
            tos = 0,
            len = 20,
            #id = 1,
            ttl = 1,
            proto = 0,
            #chksum = 34792, #ignore
            src = ipv4_veth11,
            dst = ipv4_veth21,
        )

        try:
            ## def send_packet(test, port_id, pkt, count=1)
            send_packet(self, 0, pkt1)
            verify_packets(self, pkt2, ports=[0])
        finally:
            pass

