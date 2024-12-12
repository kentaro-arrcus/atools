"""
Send Arp Request and confirm correct Reply is received.
"""
import ptf
from ptf.testutils import *
import ptf.packet as packet #scapy

import base_test

# TODO: Add class to connect to and configure DUT(switch)

class ArpReq(base_test.DutTest):
    def runTest(self):
        print("Running ArpReq")

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

        pkt1 = packet.Ether(
            dst="ff:ff:ff:ff:ff:ff",
            src=mac_veth11)
        pkt1 /= packet.ARP(
            hwsrc=mac_veth11, hwdst="00:00:00:00:00:00",
            psrc=ipv4_veth11, pdst=ipv4_veth10,
            op=1, hwlen=6, plen=4)

        pkt2 = packet.Ether(
            dst=mac_veth11,
            src=mac_veth10)
        pkt2 /= packet.ARP(
            hwsrc=mac_veth10, hwdst=mac_veth11,
            psrc=ipv4_veth10, pdst=ipv4_veth11,
            op=2, hwlen=6, plen=4)
        #pktlen = 42
        #pkt2 = pkt2 / ("\0" * (pktlen - len(pkt2)))

        try:
            ## def send_packet(test, port_id, pkt, count=1)
            send_packet(self, 0, pkt1)
            verify_packets(self, pkt2, ports=[0])
        finally:
            pass

