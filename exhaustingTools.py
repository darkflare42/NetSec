import  socket
import dns
import dns.query
import threading

TIME_INTERVAL = 10 #ms



def createTcpConnection(threadName,IP_ADDRESS,queryCheck):
    #queryCheck = dns.message.make_query('www.google.com', 2)
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

def checkIfSupportTCP(info):
    pass


def startSendIncrementTCPQueries(info):
    PORT_IN_USE = 1024

    for i in range(NumberofThreads):
        PORT_IN_USE += 1
        t=threading.Thread(target=createTcpConnection,args=("thread name %d"%(i,),'8.8.8.8',PORT_IN_USE))
        t.start()




def dnsExhaust(info):
    if checkIfSupportTCP(info)==False:
        #create string that this ns do not support Tcp connection .
    else:
        info = startSendIncrementTCPQueries(info);



