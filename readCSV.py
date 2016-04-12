import csv
import csv
from NetModule import *
from exhaustingTools import *

def urlGenerator():
    with open('C:\\Users\\Omer\\Desktop\\top.csv', 'r') as f:
        reader = csv.reader(f)
        for numberOfLine,URL in reader:
            yield URL
    yield True
#
def startExhust(exhustServerInfo):
    nsString=[]
    ns = exhustServerInfo['NS']
    for nsInfo in ns:
        dnsInfo = dnsExhaust(nsInfo)
        nsString.append(dnsInfo)
    webInfo = webExhaust(exhustServerInfo['ipv4'])
    resolverString = []
    resolver = exhustServerInfo['RESOLVER']
    for rs in resolver:
        rsInfo = dnsExhaust(rs)
        resolverString.append(rsInfo)
    return (nsString, webInfo, resolverString)



def main():
    # http_request("128.139.199.8")  # GOOGLE
    num_of_connections = test_HTTP_connection_tolerance("128.139.199.8")
    getURL=urlGenerator()
    url = next(getURL);
    while url!=True:
        url = next(getURL);
        exhustServerInfo=create_domain_dict(url)
        print(exhustServerInfo)
        return;
        infoToWrite=startExhust(exhustServerInfo)
        return
    print("finito")



main()