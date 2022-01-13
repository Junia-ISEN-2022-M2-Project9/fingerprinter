import scapy.all
from scapy.all import *
from scapy.layers.inet import UDP, TCP

pcap = rdpcap("files/onlyhttp.pcap")

filter = scapy.all.load_layer("http")


def filter_get_requests(pkg):
    return pkg.haslayer(filter)

