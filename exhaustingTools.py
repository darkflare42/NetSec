import  socket
import dns
import dns.query
import threading
import time
import NetModule
import queue
import HTTP_Tester

TIME_INTERVAL = 10 #ms
NOT_TCP = 2

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




def checkIfSupportTCP(info):
    global NOT_TCP
    try:
        print(dns.query.tcp(info[1],info[0],timeout=NOT_TCP))
    except dns.exception.Timeout:
        return False
    return True






def startSendIncrementTCPQueries(info):
   # PORT_IN_USE = 1024
    global TIME_INTERVAL
    numberOfConnection = 1
    allThread = []
    try:
        while True:
            numberOfConnection += 1
            t=threading.Thread(target=createTcpConnection, args=("thread name %d"%(numberOfConnection),info[0],info[1]))
            allThread.append(t)
            t.start()
            time.sleep(TIME_INTERVAL)
    except:
        #using flag
        [t.stop() for t in allThread]
        return numberOfConnection


def dnsExhaust(info):
    if checkIfSupportTCP(info)==False:
        return "NS %d Does not support TCP connection"%(info[0],)
    else:
        numberOfConnection = startSendIncrementTCPQueries(info);
        return "NS support TCP. Stop working after %d ."%(numberOfConnection,)





def test_HTTP_connection_tolerance(url):
    '''
    Does the same thing as the TCP Queries, but for HTTP
    :param info:
    :return: The number of HTTP connections the server allowed to open
    '''
    INTERVAL = 0.1
    num_of_connections = 0
    all_threads = []
    bucket = queue.Queue()

    while True:
        try:
            num_of_connections += 1
            thread_obj = HTTP_Tester.Threaded_Test(bucket, url)
            thread_obj.start()
            all_threads.append(thread_obj)
            time.sleep(INTERVAL)
            exc = bucket.get(block=False)
        except queue.Empty:
            pass
        else:
            exc_type, exc_obj, exc_trace = exc
            # deal with the exception
            print(exc_type, exc_obj)
            print(exc_trace)
            [thread.join(0.1) for thread in all_threads]
            return num_of_connections
            #thread_obj.join(0.1)
            # thread_obj.join()
            #return

        # thread_obj.join(0.1)
        # if thread_obj.isAlive():
        #    continue
        #else:
        #    break


    # try:
    #     while True:
    #         num_of_connections += 1
    #         thread = threading.Thread(target=NetModule.http_request, args=(info[0]))
    #         all_threads.append(thread)
    #         thread.start()
    #         thread.join()
    #         time.sleep(INTERVAL)
    # except:
    #     [thread._stop() for thread in all_threads]
    #     return num_of_connections
