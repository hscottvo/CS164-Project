from socket import *

DHCP_SERVER = ("", 67)
DHCP_CLIENT = ("255.255.255.255", 68)

available_ips = set(i for i in range(1, 255))

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Allow socket to broadcast messages
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind socket to the well-known port reserved for DHCP servers
s.bind(DHCP_SERVER)

# Recieve a UDP message
msg, addr = s.recvfrom(1024)

print(type(msg))
print(len(msg))
# Print the client's MAC Address from the DHCP header
print("Client's MAC Address is " + format(msg[28], "x"), end="")
for i in range(29, 34):
    print(":" + format(msg[i], "x"), end="")
print()
print("Transaction ID: " + ".".join(format(x, "x") for x in msg[4:8]))
print("client's current ip address: " + ".".join(format(x, "x") for x in msg[12:16]))
print("yiaddr: " + ".".join(format(x, "x") for x in msg[16:20]))
# Send a UDP message (Broadcast)

reply = b"0" * len(msg)

s.sendto(b"Hello World!", DHCP_CLIENT)
