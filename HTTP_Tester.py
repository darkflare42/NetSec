import threading
import sys
import socket
from urllib.parse import urlparse
import time
import http.client
import schedule
import CounterWrapper



CRLF = "\r\n"
GETREQUEST = "GET / HTTP/1.1" + CRLF
REQUEST_TERMINAL = "Connection: keep-alive" + CRLF + CRLF
TIME_INTERVAL = 0.1  # in seconds
ADD_CONN_INTERVAL = 2  # in seconds


class Threaded_Test(threading.Thread):
    def __init__(self, bucket, site_url, counter):
        threading.Thread.__init__(self)
        self.bucket = bucket
        self._url = site_url
        self._counter = counter
        schedule.every(ADD_CONN_INTERVAL).seconds.do(self.open_connection)
        self._connections = []
        self._stopper = threading.Event()
        self._path = "/"

    def run(self):
        self.open_connection()

        # Run a simple get operation - this allows us to change the url or the path in case we get 301 or 302 message
        h = http.client.HTTPConnection(self._url, 80)
        h.request("GET", self._path, headers={"Connection": " keep-alive"})
        r1 = h.getresponse()
        r1.read()

        if r1.status == 301:  # Moved permanently, the path has changed
            self._path = r1.getheader("Location")
        elif r1.status == 302:  # Moved temporarily, the whole url has changed
            self._url = r1.getheader("Location")

        h.close()

        while True:
            try:
                if self.stopped():
                    for h1 in self._connections:
                        h1.close()
                    break
                schedule.run_pending()
                for h1 in self._connections:
                    h1.request("GET", self._path, headers={"Connection": " keep-alive"})
                    r1 = h1.getresponse()
                    r1.read()
                    if r1.status != 200:
                        raise Exception("Server stopped responding 200 or 302")
                time.sleep(TIME_INTERVAL)

            except ConnectionError as ex:
                print("Connection error, forcibly closed")
                self.bucket.put(sys.exc_info())
                self.stopit()
                # raise Exception("Connection forcibly closed")
            except Exception as e:
                print(e)
                #print("Oops! something went wrong with HTTP testing")
                self.bucket.put(sys.exc_info())
                self.stopit()

    def open_connection(self):
        try:
            h = http.client.HTTPConnection(self._url, 80)
            self._connections.append(h)
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
