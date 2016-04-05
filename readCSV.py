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