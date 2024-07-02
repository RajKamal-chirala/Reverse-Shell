# Reverse-Shell
- A reverse shell is a type of shell session that is initiated from a remote machine, as opposed to a traditional shell, which is initiated from the local machine. In a reverse shell scenario, the remote machine connects back to the attacking machine. This technique is often used to bypass network security mechanisms, such as firewalls and NAT (Network Address Translation), which typically block incoming connections.

- Created reverse Shell using python socket library.
  
- Client.py is ran on the host that we want to connect to. This script has the ip address of the server and creates a connection to it.

- Server.py is ran form the server with a static ip address. It listens and accepts the connections coming from the client hosts.
