import json
import ast
from flask import Flask,abort
import socket
from http.server import BaseHTTPRequestHandler,HTTPServer
import time
AS_IP = '0.0.0.0'
AS_Port = 53533
buffer_size = 1024
app = Flask(__name__)


def get_fs_body(AS_IP, AS_Port):
    # Socket Programming for AS server
    AS_FS_UDP_Socket = socket.socket(family=socket.AF_INET,
                                     type=socket.SOCK_DGRAM)  # AF_INET is IPV4 , SOCK_DGRAM specifies that we use UDP instead of TCP
    AS_FS_UDP_Socket.bind((AS_IP, AS_Port))  # bind to the AS socket on which it is listning
    print("AS server is listning")
    msg_from_AS = "FS Server has successfully registered to Authoritative Server"
    send_bytes = str.encode(msg_from_AS)
    while (True):  # keep loop running so that it can recieve incoming requests
        bytes_address_pair = AS_FS_UDP_Socket.recvfrom(buffer_size)  # recieves 1024 bytes
        msg_from_fs = bytes_address_pair[0]
        FS_address = bytes_address_pair[1]  # ('127.0.0.1', 52311)
        FS_ip = bytes_address_pair[1][0]
        FS_msg = "Message from FS Server is {}".format(msg_from_fs)
        FS_ip = "IP address of FS server is {}".format(FS_ip)
        print(FS_msg)
        print(FS_ip)
        AS_FS_UDP_Socket.sendto(send_bytes, FS_address)
        return msg_from_fs


def DNS_US_Request_Response(AS_IP, AS_Port):
    AS_US_UDP_Socket = socket.socket(family=socket.AF_INET,
                                     type=socket.SOCK_DGRAM)  # AF_INET is IPV4 , SOCK_DGRAM specifies that we use UDP instead of TCP
    AS_US_UDP_Socket.bind((AS_IP, AS_Port))  # bind to the AS socket on which it is listning
    while (True):  # keep loop running so that it can recieve incoming requests
        bytes_address_pair = AS_US_UDP_Socket.recvfrom(buffer_size)  # recieves 1024 bytes
        msg_from_US = bytes_address_pair[0]
        US_address = bytes_address_pair[1]  # ('127.0.0.1', 52311)
        US_ip = bytes_address_pair[1][0]
        US_msg = "Message from US Server is {}".format(msg_from_US)
        US_ip = "IP address of US server is {}".format(US_ip)
        print(US_msg)
        print(US_ip)
        return msg_from_US, US_address, AS_US_UDP_Socket


def dns_lookup(FS_Dict, US_Dict):
    FS_Dict = str(FS_Dict, encoding='utf-8')  # converts dictionary to string
    US_Dict = str(US_Dict, encoding='utf-8')
    US_Dict = ast.literal_eval(US_Dict)  # ast module converts string into dictionary
    FS_Dict = ast.literal_eval(FS_Dict)
    if US_Dict['Type'] == FS_Dict['TYPE'] and US_Dict['Name'] == FS_Dict['NAME']:
        return 200
    else:
        return 404


def Send_Message_To_US_Server(US_Values, check_val, FS_Dict):
    US_Address = US_Values[1]
    AS_US_UDP_Socket = US_Values[2]
    if check_val == 200:
        FS_Dict = FS_Dict.decode('utf-8')
        msg_from_AS = str(FS_Dict)
        send_bytes = str.encode(msg_from_AS)  # need to convert string into bytes
        print(msg_from_AS)
        AS_US_UDP_Socket.sendto(send_bytes, US_Address)
        print("Message Sent Successfully to User Server")
        return 200
    else:
        print("Message could not be sent to User Server")
        abort(400)
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=53533)#DNS server operates on port 53

FS_Dict = get_fs_body(AS_IP, AS_Port)  # function that extracts the bytes sent by fibonacci server
US_Values = DNS_US_Request_Response(AS_IP, AS_Port)  # returns that data sent by US server and  its address
US_Dict = US_Values[0]
check_val = dns_lookup(FS_Dict, US_Dict)
print(check_val)
Send_Message_To_US_Server(US_Values, check_val, FS_Dict)







