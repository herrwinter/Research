class WrongIFNameExcpetion(Exception):
    def __init__(self, iface):
        self.msg = "Wrong interface name : {INF}".format(INF=iface)
        self.iface = iface
        self.code = -17

    def __str__(self):
        return self.msg

class IPAddressNotFoundException(Exception):
    def __init__(self, mac_addr, network):
        self.msg = "No IP address for {MAC} in {NET}".format(MAC=mac_addr, NET=network)
        self.mac_addr = mac_addr
        self.network = network
        self.code = -18

    def __str__(self):
        return self.msg

class NoIPAddressINFException(Exception):
    def __init__(self, iface):
        self.msg = "Interface [{INF}] has no IP address".format(INF=iface)
        self.iface = iface
        self.code = -19

    def __str__(self):
        return self.msg

class InvalidMACFormatException(Exception):
    def __init__(self, mac):
        self.msg = "Invalid MAC address format : {MAC}".format(mac)
        self.mac = mac
        self.code = -20

    def __str__(self):
        return self.msg
