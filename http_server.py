import network
import socket
from machine import Pin
import time
import config

# wifi info
ssid = config.ssid
password = config.pwd

# connect to wifi 
wlan = network.WLAN(network.STA_IF) # station mode (act as wifi client) | access point mode (act as router/AP)
wlan.active(True)
# wlan.scan()
wlan.connect(ssid, password)

connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() == 3: # 3 means connected -> check help(network)
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)

# check if connection successful
if wlan.status() != 3: 
    raise RuntimeError('[ERROR] Failed to establish a network connection')
else: 
    print('[INFO] CONNECTED!')
    network_info = wlan.ifconfig()
    print('[INFO] IP address:', network_info[0])

# set up socket and listen on port 80
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)  # Listen for incoming connections

print('[INFO] Listening on', addr)

# generate html
html = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <head><title>Raspberry Pi Pico Web Server</title></head>
  <body>
      <h1>HELLO, IOT 2024!</h1>
      <h2>Finally work!</h2>
  </body>
</html>
"""

# accept connections + send HTTP response
while True:
    cl, addr = s.accept()
    print('[INFO] Client connected from', addr)
    
    # receive request
    request = cl.recv(1024)
    print('[INFO] Request:', request)
    
    # send the http response to the client
    cl.send(html)
    
    # close connection
    cl.close()  
