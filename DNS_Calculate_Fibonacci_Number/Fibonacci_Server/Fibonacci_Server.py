from flask import Flask,abort
from flask import request
import socket

app = Flask(__name__)
#http://localhost:9090/register
@app.route('/register', methods=['POST'])
def Fibonacci_Num():  # put application's code here
    try:
        data=request.get_json()
        print(data)

        #UDP Socket Programming
        as_ip = data['as_ip']
        as_port = int(data['as_port'])
        fs_dict={}
        fs_dict['TYPE']='A'
        fs_dict['NAME']=data['hostname']
        fs_dict['VALUE']=data['ip']
        fs_dict['TTL']=10
        msg_from_fs=str(fs_dict)#convert dictionary to string for sending message to AS server
        bytes_sent = str.encode(msg_from_fs)
        print(msg_from_fs)
        buffer = 1024
        AS_server_address = (as_ip, as_port)  # tuple of server details
        FS_UDP_Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)# UDP socket created at FB_server
        FS_UDP_Socket.sendto(bytes_sent, AS_server_address)  # send the AS server data
        msg_from_AS_server = FS_UDP_Socket.recvfrom(buffer)
        msg = 'Message from AS_Server is: {}'.format(msg_from_AS_server[0])
        print(msg)
        return msg,201
    except:
        abort(400)
@app.route('/fibonacci')
def Calculate_Fibonacci_Number():
    try:
        num=request.args.get('number')
        num=int(num)
        sum=0
        fib0=0
        fib1=1
        fib2=1
        if num==0:
            return "The fibonacci number is : {}".format(fib0), 200
        elif num==1 or num==2:
            return "The fibonacci number is : {}".format(fib1), 200
        else:
            i=2
            for i in range(num-2):
                sum = fib1 + fib2
                fib1=fib2
                fib2=sum
            return "The fibonacci number is : {}".format(sum), 200
    except:
        return "Bad Format", 400





if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=9090)

