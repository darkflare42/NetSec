import  socket
import dns
import dns.query
import threading
import time
import NetModule
import queue
import HTTP_Tester

TIME_INTERVAL = 0.1 #ms
NOT_TCP = 2

def createTcpConnection(threadName,IP_ADDRESS,queryCheck,Bucket):
    #queryCheck = dns.message.make_query('www.google.com', 2)
    print(threadName)
    try:
        while len(Bucket) == 0:

            dns.query.tcp(queryCheck,IP_ADDRESS)
    except:
        Bucket.append(1)


def checkIfSupportTCP(info):
    global NOT_TCP
    try:
        dns.query.tcp(info[1],info[0],timeout=NOT_TCP)
    except dns.exception.Timeout:
        return False
    return True

def startSendIncrementTCPQueries(info):
   # PORT_IN_USE = 1024
    global TIME_INTERVAL
    numberOfConnection = 1
    allThread = []
    Bucket=[]
    try:
        while len(Bucket) == 0:
            numberOfConnection += 1
            t=threading.Thread(target=createTcpConnection, args=("thread name %d"%(numberOfConnection),info[0],info[1],Bucket))
            allThread.append(t)
            t.start()
            time.sleep(TIME_INTERVAL)
        print("//")
        [t.join() for t in allThread]
        print("dddd")
        return numberOfConnection
    except:
        #using flag
        [t.join() for t in allThread]
        return numberOfConnection


def dnsExhaust(info):
    if checkIfSupportTCP(info)==False:
        return "NS %s Does not support TCP connection"%(info[0],)
    else:
        numberOfConnection = startSendIncrementTCPQueries(info)
        return "NS support TCP. Stop working after %d ."%(numberOfConnection,)





def test_HTTP_connection_tolerance(url, ip):
    """
    Does the same thing as the TCP Queries, but for HTTP
    :param info:
    :return: The number of HTTP connections the server allowed to open
    """

    INTERVAL = 0.1
    num_of_connections = 0
    all_threads = []
    bucket = queue.Queue()

    while True:
        try:

            num_of_connections += 1
            if num_of_connections%40==0:
                print("Num of connections is: " + str(num_of_connections))
            thread_obj = HTTP_Tester.Threaded_Test(bucket, url, ip)
            thread_obj.start()
            all_threads.append(thread_obj)
            time.sleep(INTERVAL)
            exc = bucket.get(block=False)
        except RuntimeError as e:
            print("Runtime Error!")
        except queue.Empty:
            pass
        else:
            exc_type, exc_obj, exc_trace = exc
            # deal with the exception
            print(exc_type, exc_obj)
            print(exc_trace)
            [thread.join(0.1) for thread in all_threads]
            return num_of_connections
