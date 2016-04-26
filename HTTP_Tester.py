import threading
import sys
import socket
from urllib.parse import urlparse
import time
import http.client
import schedule
import CounterWrapper
#from exhaustingTools import lock
import exhaustingTools
from io import BytesIO


CRLF = "\r\n"
GETREQUEST = "GET / HTTP/1.1" + CRLF
REQUEST_TERMINAL = "Connection: keep-alive" + CRLF + CRLF
TIME_INTERVAL = 0.1  # in seconds
ADD_CONN_INTERVAL = 2  # in seconds
PORT = 80

class Threaded_Test(threading.Thread):
    def __init__(self, bucket, site_url, ip, counter):
        threading.Thread.__init__(self)
        self.bucket = bucket
        self._url = "www." + site_url
        self._counter = counter
        self._job = schedule.every(ADD_CONN_INTERVAL).seconds.do(self.open_connection)
        self._connections = []
        self._stopper = threading.Event()
        self._path = "/"
        self._ip = socket.gethostbyname(site_url)


    def run(self):

        site_ip = urlparse(self._ip)
        # path = site_ip.path


        # if path == "":
        #   path = "/"

        # HOST = url[2]
        HOST = site_ip[2]
        #HOST = self._ip

        request = GETREQUEST + "Host: " + self._url + CRLF + REQUEST_TERMINAL
        sock = None

        # Try first connection to check if the url or path is different than the standard root and given url

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # sock.settimeout(0.30)
            # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.connect((HOST, PORT))

            sock.send(request.encode())
            response = http.client.HTTPResponse(sock)
            response.begin()
            response.read()
            #data = (sock.recv(1000000))

            #source = FakeSocket(data)
            #response = http.client.HTTPResponse(source)
            #response.begin()
            if response.status == 301:
                self._path = response.getheader("Location")
            elif response.status == 302:
                self._url = response.getheader("Location")
                temp = urlparse(self._url)
                self._ip = socket.gethostbyname_ex(temp[1])
                self._path = temp[2]

            #sock.shutdown(1)
            #sock.close()
        except Exception as ex:
            print("Could not open new socket")
            self.bucket.put(sys.exc_info())

        data = []

        request = self.createRequestString(self._url, self._path)
        self.open_connection()
        while not self._stopper.isSet():
            try:
                if self._stopper.isSet():
                    schedule.cancel_job(self._job)
                    schedule.clear()
                    #for sock in self._connections:
                    #    sock.shutdown(1)
                    #    sock.close()
                    break
                schedule.run_pending()
                for sock in self._connections:
                    try:
                        sock.send(request.encode())
                        response = http.client.HTTPResponse(sock)
                        response.begin()
                        response.read()

                        #data = (sock.recv(8192))

                        #if data == "":
                        #    raise Exception("Server closed the connection")
                        # temp = data.decode("utf-8")
                        #source = FakeSocket(data)
                        #response = http.client.HTTPResponse(source)
                        #response.begin()
                        if response.status != 200:
                            raise Exception("Server stopped responding 200 OK")
                    except Exception as ex:
                        print(ex)
                        raise Exception("Failure to send request or decrypt response")

                # print(response.status, response.code)
                time.sleep(TIME_INTERVAL)
            except Exception as ex:
                # print("Connection forcibly closed, could not send request")
                print(ex)
                self.stopit()
                schedule.cancel_job(self._job)
                #for sock in self._connections:
                #    sock.shutdown(1)
                #    sock.close()
                self.bucket.put(sys.exc_info())
                # raise Exception("Connection forcibly closed")

        print("Closing Sockets")
        for sock in self._connections:
           sock.shutdown(socket.SHUT_RDWR)
           sock.close()
        print("Finished closing sockets " + str(len(self._connections)))






    def run2(self):
        # self.open_connection()

        # Run a simple get operation - this allows us to change the url or the path in case we get 301 or 302 message
        try:
            h = http.client.HTTPConnection(self._url, 80, timeout=10)
            # h.
            h.request("GET", self._path, headers={"Connection": " keep-alive"})
            r1 = h.getresponse()
            r1.read()

            if r1.status == 301:  # Moved permanently, the path has changed
                self._path = r1.getheader("Location")
            elif r1.status == 302:  # Moved temporarily, the whole url has changed
                self._url = r1.getheader("Location")

            h.close()
        except:
            raise Exception("Failed on first connection")

        while True:
            try:
                if self._stopper.isSet():
                    schedule.cancel_job(self._job)
                    for h1 in self._connections:
                        h1.close()
                    break
                    #return
                schedule.run_pending()
                for h1 in self._connections:
                    try:

                        h1.request("GET", self._path, headers={"Connection": " keep-alive"})
                    except http.client.CannotSendRequest:
                        print("Could not send request")
                        raise Exception("Previous response was not received")

                    r1 = h1.getresponse()
                    r1.read()
                    if r1.status != 200:
                        raise Exception("Server stopped responding 200 or 302")
                time.sleep(TIME_INTERVAL)

            except ConnectionError as ex:
                print("Connection error, forcibly closed")
                self.bucket.put(sys.exc_info())
                self.bucket.put(ex)
                # self.stopit()
                # raise Exception("Connection forcibly closed")
            except Exception as e:
                print(e)
                #print("Oops! something went wrong with HTTP testing")
                self.stopit()
                self.bucket.put(sys.exc_info())
                self.bucket.put(e)

    def open_connection(self):
        try:
            if not self._stopper.isSet():
                print("Adding HTTP Socket")
                with exhaustingTools.lock:
                    self._counter.increment()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(180)
                # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                sock.connect((self._ip, PORT))
                self._connections.append(sock)
                print("Added HTTP Socket")

        except Exception as ex:
            print(ex)
            print("Connection error, Could not open new connection")
            self.stopit()
            schedule.cancel_job(self._job)
            schedule.clear()
            #for sock in self._connections:
            #    sock.shutdown(1)
            #    sock.close()
            self.bucket.put(sys.exc_info())




    def open_connection2(self):
        try:
            h = http.client.HTTPConnection(self._url, 80, timeout=10)
            self._connections.append(h)
            with exhaustingTools.lock:
                self._counter.increment()

        except:
            print("Connection error, Could not open new connection")
            self.bucket.put(sys.exc_info())
            self.stopit()
            # raise Exception("Connection not possible")

    def stopit(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.isSet()

    def createRequestString(self, host, path):
        return "GET " + path + " HTTP/1.1" + CRLF + "Host: " + host + CRLF + REQUEST_TERMINAL


class FakeSocket(BytesIO):
    def __init__(self, response_str):
        self._file = BytesIO(response_str)

    def makefile(self, *args, **kwargs):
        return self._file
