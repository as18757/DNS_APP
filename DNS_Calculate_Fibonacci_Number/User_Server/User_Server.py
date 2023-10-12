import urllib.request

from flask import Flask,abort,request,redirect
import ast
#localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=8&as_ip=127.0.0.1&as_port=53533
#http://10.0.0.142:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=8&as_ip=127.0.0.1&as_port=53533
import socket
app = Flask(__name__)
@app.route('/fibonacci')
def US_Server():  # put application's code here
    hostname=request.args.get('hostname')#gets the argument form the request query
    fs_port=request.args.get('fs_port')
    fs_port=int(fs_port)#convert the string sent into integer
    number=request.args.get('number')
    number=int(number)
    as_ip=request.args.get('as_ip')
    as_port=request.args.get('as_port')
    as_port=int(as_port)
    DNS_req_dict={}
    #creating a request
    DNS_req_dict['Type']='A'
    DNS_req_dict['Name']=hostname
    # condition to validate query
    if hostname is not None and fs_port is not None and number is not None and as_ip is not None and as_port is not None:
        # UDP Socket Programming

        DNS_query=str(DNS_req_dict)
        bytes_sent=str.encode(DNS_query)
        buffer=1024
        US_UDP_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        AS_Address=(as_ip,as_port)
        US_UDP_Socket.sendto(bytes_sent,AS_Address)
        DNS_Response_AS_Server=US_UDP_Socket.recvfrom(buffer)
        msg = 'Message from AS_Server is {}'.format(DNS_Response_AS_Server[0])
        FS_Details=DNS_Response_AS_Server[0].decode('utf-8')
        print("Successfully recieved IP address")
        FS_Detail=ast.literal_eval(FS_Details)#converts string to dictionary
        FS_IP=str(FS_Detail['VALUE'])
        FibonacciRequestString="http://"+FS_IP+":"+str(fs_port)+"/fibonacci?number="+str(number)
        FibonacciAnswer=urllib.request.urlopen(FibonacciRequestString)#the urllib function gets all the details from the FS url
        return FibonacciAnswer, 200
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8080)

