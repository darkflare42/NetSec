import csv
import csv
from NetModule import *
from exhaustingTools import *
Domain = 'Domain'
ns = 'Name Servers'
ws = 'Web Servers'
dns = 'DNS Servers'
headers=[Domain,ns, ws, dns]

def urlGenerator():
    with open('C:\\Users\\Omer\\Desktop\\top.csv', 'r') as f:
        reader = csv.reader(f)
        for numberOfLine,URL in reader:
            yield URL
    yield True
#
#
def startExhust(exhustServerInfo):
    print(exhustServerInfo)
    nsString=[]
    print(str(exhustServerInfo['ipv4']))
    webInfo = test_HTTP_connection_tolerance(exhustServerInfo["DOM"], str(exhustServerInfo['ipv4']))
    wbSt='wsInfo: %d' % (webInfo,)
    print(wbSt)

    resolverString = []
    resolver = exhustServerInfo['RESOLVER']
    for rs in resolver:
        rsInfo = dnsExhaust(rs)
        rsSt= 'dns info %s: %d' % (rs,rsInfo)
        resolverString.append(rsInfo)


    return #TODO CHANGE
    ns = exhustServerInfo['NS']
    for nsInfo in ns:
        dnsInfo = dnsExhaust(nsInfo)
        stDns='nsInfo %s: %d'%(ns, dnsInfo)
        nsString.append(stDns)


    return {'nsInfo' : nsString, 'webInfo' : wbSt, 'resInfo' : resolverString}



def main():
    # http_request("128.139.199.8")  # GOOGLE
    num_of_connections = test_HTTP_connection_tolerance("www.google.com" ,"128.139.199.8")  # OR: This is to test the http tolerance
    getURL=urlGenerator()
    url = next(getURL);
    writeToFile=csv.DictWriter(open('file3.csv','w'), delimiter=',',lineterminator='\n', fieldnames=headers)
    writeToFile.writerow({Domain:Domain,ns:ns,ws:ws,dns : dns})
    while url!=True:
        exhustServerInfo=create_domain_dict(url)
        infoToWrite=startExhust(exhustServerInfo)
        writeToFile.writerow({Domain : url, ns : infoToWrite['nsInfo'], ws : infoToWrite['webInfo'] , dns:infoToWrite['resInfo']})
        url = next(getURL);
        return# TODO MOVE THIS SHIT
main()
