import threading
import sys
import socket
import urllib.parse
import time

CRLF = "\r\n\r\n"
GETREQUEST = "GET / HTTP/1.1" + CRLF + "Connection: keep-alive" + CRLF + CRLF
TIME_INTERVAL = 0.05  # ms

class Threaded_Test(threading.Thread):
    def __init__(self, bucket, site_url):
        threading.Thread.__init__(self)
        self.bucket = bucket
        self._url = site_url

    def run(self):
        url = urllib.parse.urlparse(self._url)
        path = url.path

        if path == "":
            path = "/"

        HOST = url[2]
        PORT = 80

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.30)
            # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.connect((HOST, PORT))
        except:
            self.bucket.put(sys.exc_info())
            # raise Exception("Connection not possible")
        data = []

        while True:
            try:
                sock.send(GETREQUEST.encode())
                data = (sock.recv(1000000))
                time.sleep(TIME_INTERVAL)
            except:
                self.bucket.put(sys.exc_info())
                # raise Exception("Connection forcibly closed")

        print(data.decode())

        # sock.shutdown(1)
        # sock.close()
        # try:
        #     raise Exception('An error occured here.')
        # except Exception:
        #     self.bucket.put(sys.exc_info())

