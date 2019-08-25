from scapy.all import *
from threading import Thread, Event


class RSSISniffer(Thread):

    FILE_EXT = '.pcap'

    def __init__(self, target_address, file_name, interface, max_packet_number=100):

        super().__init__()

        self.daemon = True  # This thread dies when main thread exits.
        self.socket = None  # To release resources(sniff socket)
        self.iface = interface
        self.stop_sniffing = Event()
        self.file_name = file_name
        self.max_packet_num = max_packet_number
        self.target_address = target_address
        self.pkts = []
        self.rssis = []
        self.latest_rssi = None

        self._number_of_packets = None  # read-only

    @property
    def number_of_packets(self):
        return len(self.pkts)

    def run(self):
        self.socket = conf.L2listen(
            type=ETH_P_ALL,
            iface=self.iface
        )

        sniff(
            opened_socket=self.socket,
            prn=self.packet_handler,
            stop_filter=self.should_stop_sniffing
        )

        if len(self.rssis) == 0:
            return

        self.save_packet()
        self.save_rssi()

        print("[*] CNT : {CNT}, MAX : {MAX}, MIN : {MIN}, AVE : {AVE}\n".format(CNT=self.number_of_packets,
                                                                                MAX=max(self.rssis),
                                                                                MIN=min(self.rssis),
                                                                                AVE=self.get_average_rssi()))

        sys.exit()

    def get_average_rssi(self):
        size = len(self.rssis)
        return 0 if size == 0 else round(sum(self.rssis, 0.0) / size, 2)

    def get_latest_rssi(self):
        return self.latest_rssi

    def join(self, timeout=None):
        self.stop_sniffing.set()
        super().join(timeout)

    def stop(self):
        self.join(1.0)

    def save_packet(self):
        wrpcap(self.file_name + self.FILE_EXT, self.pkts)

    def save_rssi(self):
        f = open(self.file_name + '_RSSI.txt', 'a')

        f.write("[*] CNT : {CNT}, MAX : {MAX}, MIN : {MIN}, AVE : {AVE}\n".format(CNT=self.number_of_packets,
                                                                                  MAX=max(self.rssis),
                                                                                  MIN=min(self.rssis),
                                                                                  AVE=self.get_average_rssi()))

        idx = 0
        for rssi in self.rssis:
            f.write(str(rssi) + ' ')
            idx += 1
            if idx % 10 == 0:
                f.write('\n')
                idx = 0

        f.close()

    def should_stop_sniffing(self, pkt):
        return self.stop_sniffing.isSet()

    def packet_handler(self, pkt):
        if not pkt.haslayer(RadioTap):
            return

        # data or control frame
        if not (pkt.type == 2 or pkt.type == 1):
            return

        # if it's from target
        if pkt.addr2 == self.target_address:
            self.pkts.append(pkt)
            self.rssis.append(pkt.dBm_AntSignal)
            self.latest_rssi = pkt.dBm_AntSignal

        # stop sniffing
        if self.number_of_packets >= self.max_packet_num:
            self.stop_sniffing.set()
