"""
L3 IPv4 forwarding TTL test. Expect TTL expired.
"""
import ptf
from ptf.testutils import *
import ptf.packet as p #scapy

import base_test

class L3TtlExpired(base_test.DutTest):
    def runTest(self):
        print("Running:", self.__class__.__name__)

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
            src = ipv4_veth11,
            dst = ipv4_veth21,
        )

        pkt2 = p.Ether(
            src = mac_veth10,
            dst = mac_veth11,
        )
        pkt2 /= p.IP(
            ttl = 64,
            src = ipv4_veth10,
            dst = ipv4_veth11,
        )
        pkt2 /= p.ICMP(
            type = 11, #Time Exceeded
            #chksum = 62719, #ignore
        )
        pkt2 /= pkt1.payload

        m = ptf.mask.Mask(pkt2)
        m.set_do_not_care_scapy(IP, 'tos')
        m.set_do_not_care_scapy(IP, 'id')
        m.set_do_not_care_scapy(IP, 'chksum')

        try:
            ## def send_packet(test, port_id, pkt, count=1)
            send_packet(self, 0, pkt1)
            #verify_packets(self, pkt2, ports=[0])
            verify_packets(self, m, ports=[0])
        finally:
            pass

