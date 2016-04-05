import  socket
import dns
import dns.query
import threading



def createTcpConnection(threadName,IP_ADDRESS,SOURCE_PORT):
    queryCheck = dns.message.make_query('www.google.com', 2)
    while True:
        print(threadName)
        print(dns.query.tcp(queryCheck,IP_ADDRESS))

# def portIsOpen(portNum):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     result = sock.connect_ex(('127.0.0.1', portNum))
#     print(result)
#     if result == 0:
#         return True;
#     return False


def createThreads(NumberofThreads):
    PORT_IN_USE = 1024
    for i in range(NumberofThreads):
        # while (portIsOpen(PORT_IN_USE) == False):
        #     PORT_IN_USE += 1
        PORT_IN_USE += 1
        t=threading.Thread(target=createTcpConnection,args=("thread name %d"%(i,),'8.8.8.8',PORT_IN_USE))
        t.start()


createThreads(40)
# def checkIfTcp(serverAddress):
#   #  try:sdf
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_address=(serverAddress,10000);
#         sock.connect(server_address)
#     #except:
#         print("h")
#
# #checkIfTcp('www.google.co.il')
#
#
#
#
# s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# result = s.connect_ex(('113.165.88.235 ', 10000))
# s.close()
# if result > 0:
#     print("problem with socket!")
# else:
#     print("everything it's ok!")