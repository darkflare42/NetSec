import threading
import sys
import socket
import urllib.parse
import time
import http.client


CRLF = "\r\n"
GETREQUEST = "GET / HTTP/1.1" + CRLF
REQUEST_TERMINAL = "Connection: keep-alive" + CRLF + CRLF
TIME_INTERVAL = 10  # ms


class Threaded_Test(threading.Thread):
    def __init__(self, bucket, site_url, ip):
        threading.Thread.__init__(self)
        self.bucket = bucket
        self._url = site_url
        self._ip = ip

    def run(self):

        site_ip = urllib.parse.urlparse(self._ip)
        path = site_ip.path

        # url = urllib.parse.urlparse(self._url)
        # path = url.path

        if path == "":
            path = "/"

        # HOST = url[2]
        HOST = site_ip[2]
        PORT = 80
        request = GETREQUEST + "Host: " + self._url + CRLF + REQUEST_TERMINAL
        sock = None
        try:

            h1 = http.client.HTTPConnection(self._url, 80)

            # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # sock.settimeout(0.30)
            #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            # sock.connect((HOST, PORT))
        except:
            self.bucket.put(sys.exc_info())
            # raise Exception("Connection not possible")
        data = []

        testmsg = "HELLO"

        while True:
            try:
                h1.request("GET", "/home/0,7340,L-8,00.html")
                r1 = h1.getresponse()
                r1.read()
                #print(r1.status , r1.reason)
                if(r1.status != 200):
                    raise Exception("Server stopped responding 200")
                # sock.send(testmsg.encode())
                #sock.send(request)
                #sock.send(request.encode())
                #data = (sock.recv(1000000))
                #print(data)
                time.sleep(TIME_INTERVAL)
            except ConnectionError as ex:
                print("Server stopped responding 200")
                self.bucket.put(sys.exc_info())
                # raise Exception("Connection forcibly closed")

        # print(data.decode())

        # sock.shutdown(1)
        # sock.close()
        # try:
        #     raise Exception('An error occured here.')
        # except Exception:
        #     self.bucket.put(sys.exc_info())

