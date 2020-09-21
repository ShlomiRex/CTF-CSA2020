import scapy
from scapy.all import *

server = "52.28.255.56"

request = Ether()/IP(dst=server)/TCP(dport=80)/"Test"
hexdump(request)
send(request)