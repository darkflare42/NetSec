import threading
import sys
import socket
import urllib.parse
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
        self._stop = threading.Event()

    def run(self):
        self.open_connection()

        while True:
            try:
                if self.stopped():
                    break
                schedule.run_pending()
                for h1 in self._connections:
                    h1.request("GET", "/", headers={"Connection": " keep-alive"})
                    r1 = h1.getresponse()
                    r1.read()
                    print(r1.status, r1.reason)
                    if r1.status != 200:
                        raise Exception("Server stopped responding 200")
                time.sleep(TIME_INTERVAL)

            except ConnectionError as ex:
                print("Connection error, forcibly closed")
                self.bucket.put(sys.exc_info())
                self.stop()
                # raise Exception("Connection forcibly closed")
            except Exception as e:
                print(e)
                #print("Oops! something went wrong with HTTP testing")
                self.bucket.put(sys.exc_info())
                self.stop()

    def open_connection(self):
        try:
            h = http.client.HTTPConnection(self._url, 80)
            self._connections.append(h)
            self._counter.increment()
        except:
            print("Connection error, Could not open new connection")
            self.bucket.put(sys.exc_info())
            self.stop()
            # raise Exception("Connection not possible")

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
