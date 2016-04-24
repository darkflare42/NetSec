import csv
from NetModule import *
from exhaustingTools import *
import sys

Domain = 'Domain'
ns = 'Name Servers[SupportTCP][StoppedAfter]'
ws = 'Web Server: Num of concurrent connections'
dns = 'Resolvers[SupportTCP][StoppedAfter]'
headers=[Domain, dns, ns, ws]

def printUsage():
    print("=======================")
    print("This program attempts to exhaust a url's DNS Resolvers, Nameservers and HTTP Web Server")
    print("USAGE: readCSV input.csv output.csv")
    print("Where input.csv is a csv file in the format of an ALEXA TOP X csv file")
    print("=======================")


def urlGenerator(filePath):
    with open(filePath, 'r') as f:
        reader = csv.reader(f)
        for numberOfLine, URL in reader:
            yield URL
    yield True
#
#
def startExhust(exhustServerInfo):
    nsString=[]
    #TODO OR PLEASE MAKE SURE THE Http tool return any value you want. this value will be written to the "file3.csv
    # at the folder of the running python files. best of luck
    #Omer Ornan- English Teacher and sexual Instructor.
    webInfo = test_HTTP_connection_tolerance(exhustServerInfo["DOM"])
    wbSt = str(exhustServerInfo["ipv4"]) + ': %d' % (webInfo,)
    print(wbSt)
    print("hh")
    resolverString = []
    resolver = exhustServerInfo['RESOLVER']
    for rs in resolver:
        rsInfo = dnsExhaust(rs)
        print(rsInfo)
        print(rs[0])
        rsSt= 'dns info %s: %s' % (rs[0],rsInfo)
        resolverString.append(rsInfo)

    ns = exhustServerInfo['NS']
    print("dfg")
    for nsInfo in ns:
        print("dfgjj")
        dnsInfo = dnsExhaust(nsInfo)
        # stDns='nsInfo %s: %s'%(nsInfo[0], dnsInfo)
        #stDns = "%s: %s" %(nsInfo[0], dnsInfo)
        nsString.append(dnsInfo)
    return {'nsInfo' : nsString, 'webInfo' : wbSt, 'resInfo' : resolverString}



def main(argv):
    # http_request("128.139.199.8")  # GOOGLE

    # bucket = queue.Queue()
    # counter = CounterWrapper.CounterWrapper()
    # thread_obj = HTTP_Tester.Threaded_Test(bucket, 'ynet.co.il', counter)
    # thread_obj.start()
    #time.sleep(10000)
    # thread_obj.stop()
    # thread_obj.join(0.1)
    #num_of_connections = test_HTTP_connection_tolerance("www.ynet.co.il" ,"128.139.199.8")  # OR: This is to test the http tolerance

    if(len(argv) != 3):
        printUsage()
        exit(1)

    getURL=urlGenerator(argv[1])
    url = next(getURL)
    with open(argv[2], "w") as csvFile:
        writeToFile = csv.DictWriter(csvFile, delimiter=',',lineterminator='\n', fieldnames=headers)
        writeToFile.writerow({Domain: Domain, dns: dns, ns: ns, ws: ws})
    while url!=True:
        exhustServerInfo=create_domain_dict(url)
        infoToWrite=startExhust(exhustServerInfo)
        with open(argv[2], "a") as csvFile:
            writeToFile = csv.DictWriter(csvFile, delimiter=',', lineterminator='\n', fieldnames=headers)
            writeToFile.writerow({Domain : url, ns : "\r\n".join(infoToWrite['nsInfo']), dns: "\r\n".join(infoToWrite['resInfo']), ws : infoToWrite['webInfo']})
        url = next(getURL)
        # return# TODO MOVE THIS SHIT

# main()
if __name__ == "__main__":
        main(sys.argv)
