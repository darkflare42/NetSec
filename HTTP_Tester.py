import threading
import sys
import socket
import urllib.parse
import time

CRLF = "\r\n"
GETREQUEST = "GET / HTTP/1.1" + CRLF
REQUEST_TERMINAL = "Connection: keep-alive" + CRLF + CRLF
TIME_INTERVAL = 1  # ms


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
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # sock.settimeout(0.30)
            #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.connect((HOST, PORT))
        except:
            self.bucket.put(sys.exc_info())
            # raise Exception("Connection not possible")
        data = []



        while True:
            try:
                # sock.send(request.encode())
                data = (sock.recv(1000000))
                print(data)
                time.sleep(TIME_INTERVAL)
            except:
                self.bucket.put(sys.exc_info())
                # raise Exception("Connection forcibly closed")

        # print(data.decode())

        # sock.shutdown(1)
        # sock.close()
        # try:
        #     raise Exception('An error occured here.')
        # except Exception:
        #     self.bucket.put(sys.exc_info())

