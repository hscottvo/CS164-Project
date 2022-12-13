from socket import *

DHCP_SERVER = ("", 67)
DHCP_CLIENT = ("255.255.255.255", 68)

subnet = [192, 168, 0]
server_ip = subnet + [1]

available_hosts = set(i for i in range(1, 256))
open_requests = set()
cached_ip = {"server": str(server_ip)}
available_hosts.remove(1)

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
    mac_address = msg[28:34]
    mac_address_string = ":".join(format(i, "x") for i in list(mac_address))
    magic_cookie = list(msg)[236:240]

    reply = [0] * len(msg)
    # request -> ack
    # if mac_address in open_requests:
    if list(msg)[242] == 3:
        print("Got request from mac address " + mac_address_string + ". Sending ack")
        yiaddr = msg[16:20]
        ip_bytes = list(yiaddr)
        cached_ip[mac_address_string] = str(ip_bytes)
        message_type = 5

    # discover -> offer
    else:
        print("Got discover from mac address " + mac_address_string + ". Sending offer")
        open_requests.add(mac_address)
        host = available_hosts.pop()
        ip_bytes = subnet + [host]
        yiaddr = bytes(ip_bytes)
        cached_ip[mac_address_string] = str(ip_bytes)
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
        + reply[44:236]
	+ magic_cookie 
        + [0] * 192
        + [53, 1, message_type]
        + [1, 4, 255, 255, 255, 0]
        + [3, 4, 192, 168, 0, 1]
        + [54, 4, 192, 168, 0, 1]
    )

    print("Sending. Currently cached ip's: ")
    for i, j in cached_ip.items():
        print(
            "\tMac address: ",
            i,
            "\n\tip address: ",
            ".".join(j.strip("[]").split(", ")),
            sep="",
            end="\n\n",
        )

    # Send a UDP message (Broadcast)
    s.sendto(bytes(reply), DHCP_CLIENT)
