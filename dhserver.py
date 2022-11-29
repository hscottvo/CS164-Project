from socket import *

DHCP_SERVER = ("", 67)
DHCP_CLIENT = ("255.255.255.255", 68)

subnet = [192, 168, 0]
server_ip = subnet + [1]

available_hosts = set(i for i in range(1, 255))
open_requests = set()
cached_ip = set()

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Allow socket to broadcast messages
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind socket to the well-known port reserved for DHCP servers
s.bind(DHCP_SERVER)

while True:
    # Recieve a UDP message
    msg, addr = s.recvfrom(1024)
    transaction_id = msg[4:8]
    mac_address = msg[28:44]

    reply = [0] * len(msg)
    # request -> ack
    if mac_address in open_requests:
        print("Got request from mac address " + str(mac_address) + ". Sending ack")
        yiaddr = msg[16:20]
        ip_bytes = list(yiaddr)
        cached_ip.add(str(ip_bytes))
        message_type = 5

    # discover -> offer
    else:
        print("got discover from mac address " + str(mac_address) + ". Sending offer")
        open_requests.add(mac_address)
        host = available_hosts.pop()
        ip_bytes = subnet + [host]
        yiaddr = bytes(ip_bytes)
        cached_ip.add(str(ip_bytes))
        message_type = 2

    reply = (
        [2, 1, 6]
        + [reply[3]]
        + list(transaction_id)
        + reply[8:16]
        + ip_bytes
        + server_ip
        + reply[24:28]
        + list(mac_address)
        + reply[44:240]
        + [0] * 192
        + [53, 1, message_type]
        + [1, 4, 255, 255, 255, 0]
        + [3, 4, 192, 168, 0, 1]
        + [54, 4, 192, 168, 0, 1]
    )

    print("Sending. Currently cached ip's: ")
    for i in open_requests:
        # print(f"\t{list(mac_address)}")
        print("\t", i, sep="")

    # Send a UDP message (Broadcast)
    s.sendto(bytes(reply), DHCP_CLIENT)
