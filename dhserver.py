from socket import *

DHCP_SERVER = ("", 67)
DHCP_CLIENT = ("255.255.255.255", 68)

subnet = [192, 168, 0]
server_ip = subnet + [1]

available_hosts = set(i for i in range(1, 255))
open_requests = set()

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
    mac_address = list(msg[28:44])
    msg_list = list(msg)
    for i in range(len(msg)//4):
	    print(i, list(msg[i*4:min(i*4+4, len(msg))]))

    print(list(msg))

    reply = [0] * len(msg)
    # request
    if transaction_id in open_requests:
        print("Got request from transaction id " + str(list(transaction_id)) + ". Sending ack")
        yiaddr = msg[16:20]

    # discover
    else:
        print(
            "got discover from transaction id " + str(list(transaction_id)) + ". Sending offer"
        )
        open_requests.add(transaction_id)
        host = available_hosts.pop()
        ip_bytes = subnet + [host]
        yiaddr = bytes(ip_bytes)

    assert len(transaction_id) == 4
    assert len(yiaddr) == 4
    reply = (
        [2, 1]
        + [6]
        + [reply[3]]
        + list(transaction_id)
        + reply[8:16]
        + ip_bytes
	+ server_ip
	+ reply[24:28]
	+ mac_address
	+ reply[44:]
    )
    # Send a UDP message (Broadcast)
    s.sendto(bytes(reply), DHCP_CLIENT)
    # s.sendto(bytes(reply), ('.'.join(str(i) for i in mac_address[:4]), 68))
