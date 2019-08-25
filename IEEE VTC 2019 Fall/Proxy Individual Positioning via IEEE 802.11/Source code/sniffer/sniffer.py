import argparse
import os
import cursor
from time import sleep
from rssi_sniffer import RSSISniffer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect RSSI from target's data & control frame.")
    parser.add_argument('-i', help="interface name", required=True)
    parser.add_argument('-f', help="file name", default="RSSI.pcap")
    parser.add_argument('--target', help="target mac address", required=True)
    parser.add_argument('-n', help="maximum number of packets", default=1000)

    args = parser.parse_args()
    sniffer = RSSISniffer(interface=args.i, file_name=args.f, target_address=args.target, max_packet_number=int(args.n))

    cursor.hide()
    os.system('clear')
    print("[*] Start sniffing(quit : CTRL + C)...\n")
    sniffer.start()

    while sniffer.number_of_packets < sniffer.max_packet_num:
        try:
            print("\033[4;1H" + "[!] RSSI : {RSSI}".format(RSSI=str(sniffer.latest_rssi)))
            print("\033[3;1H" + "[!] Current average RSSI : {AVE}\n".format(AVE=sniffer.get_average_rssi()))
            print("\033[2;1H" + "[!] Current received packet number : {NUM}\n".format(NUM=sniffer.number_of_packets))
            sleep(0.1)

        except KeyboardInterrupt:
            break

    print("[*] Stop sniffing")
    sniffer.stop()
    cursor.show()

    if sniffer.isAlive():
        sniffer.socket.close()
