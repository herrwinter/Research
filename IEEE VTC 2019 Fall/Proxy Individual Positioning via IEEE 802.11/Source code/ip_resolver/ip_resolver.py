import threading
from time import sleep
import re
from scapy.all import *
import netifaces as ni
import netaddr
from ip_resolve_exceptions import *


class IPResolver:

    SEND_INTERVAL = 0.025
    RECEIVE_TIMEOUT = SEND_INTERVAL * 510
    MAC_RE = re.compile("^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$")

    def __init__(self, iface):
        self.iface = iface
        self.target_ip = None
        self.__target_mac = None
        self.my_mac = self.get_mac()
        self.my_ip_network = self.get_ip_cidr()

        self.sender_thread = threading.Thread(target=self.send)
        self.sender_thread.daemon = True

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.daemon = True


    @property
    def iface(self):
        return self.__iface

    @iface.setter
    def iface(self, iface):
        if iface not in ni.interfaces():
            raise WrongIFNameExcpetion(iface)

        self.__iface = iface

    @property
    def target_mac(self):
        return self.__target_mac

    @target_mac.setter
    def target_mac(self, mac):
        if not ni.AF_INET in ni.ifaddresses(self.iface):
            raise NoIPAddressINFException(self.iface)

        self.__target_mac = mac

    def resolve_ip(self, target_mac):
        if not MAC_RE.match(target_mac):
            raise InvalidMACFormatException(target_mac)

        self.target_mac = target_mac

        self.receive_thread.start()
        self.sender_thread.start()
        self.receive_thread.join()
        self.sender_thread.join(self.SEND_INTERVAL)

        if not self.target_ip:
            raise IPAddressNotFoundException(self.target_mac, str(self.my_ip_network))

        return self.target_ip

    def get_mac(self):
        return ni.ifaddresses(self.iface)[ni.AF_LINK][0]['addr']

    def get_ip_cidr(self):
        ip = ni.ifaddresses(self.iface)[ni.AF_INET][0]['addr']
        netmask = ni.ifaddresses(self.iface)[ni.AF_INET][0]['netmask']
        return netaddr.IPNetwork('{IP}{MASK}'.foramt(IP=ip, MASK=netmask))

    def receive(self):
        filter_str = "ether src " + self.target_mac + " and ether dst " + self.my_mac + " and arp"
        pkts = sniff(iface=self.iface, filter=filter_str, count=1, timeout=self.RECEIVE_TIMEOUT)

        if not pkts:
            return

        self.target_ip = pkts[0].psrc
        print(pkts[0].show())

    def send(self):
        packet = Ether(dst=self.target_mac) / ARP(op=1)
        ip_set = netaddr.IPSet(self.my_ip_network)

        ip_set.remove(self.my_ip_network.network)
        ip_set.remove(self.my_ip_network.broadcast)

        while not self.target_ip:
            for ip in ip_set:
                packet.pdst = str(ip)
                sendp(packet, iface=self.iface, verbose=False)
                sleep(self.WAIT_TIME)
