import  socket
import dns
import dns.query
import threading
import time
import NetModule
import queue
import HTTP_Tester
import CounterWrapper

TIME_INTERVAL = 0.1 #ms
NOT_TCP = 2
MAX_THREADS = 5

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
    except:
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
    if checkIfSupportTCP(info) == False:
        #return "NS %s Does not support TCP connection"%(info[0],)
        return "%s [NO][0]" % (info[0],)
    else:
        numberOfConnection = startSendIncrementTCPQueries(info)
        # return "NS support TCP. Stop working after %d ."%(numberOfConnection,)
        return "%s [YES][%d]" % (info[0], numberOfConnection)



lock = threading.Lock()

def test_HTTP_connection_tolerance(url, ip):
    """
    Does the same thing as the TCP Queries, but for HTTP
    :param info:
    :return: The number of HTTP connections the server allowed to open
    """

    INTERVAL = 0.1
    num_of_threads = 0
    all_threads = []
    bucket = queue.Queue()
    counter = CounterWrapper.CounterWrapper()
    stop_adding_threads = False


    while True:
        try:
            if num_of_threads % 40 == 0:
                print("Num of threads is: " + str(num_of_threads))
            if num_of_threads <= MAX_THREADS and (not stop_adding_threads):
                thread_obj = HTTP_Tester.Threaded_Test(bucket, url, ip, counter)
                thread_obj.start()
                all_threads.append(thread_obj)
                num_of_threads += 1
            time.sleep(INTERVAL)
            exc = bucket.get(block=False)
        except RuntimeError as e:  # This is presumably because we reached the max num of threads
            print("Runtime Error!")
            stop_adding_threads = True
        except queue.Empty:
            pass
        else:
            print("Got Exception from HTTP!")
            # exc_type, exc_obj, exc_trace = exc

            # deal with the exception
            #print(exc_type, exc_obj)
            #print(exc_trace)
            [thread.stopit() for thread in all_threads]
            [thread.join() for thread in all_threads]
            return counter.get_value()
