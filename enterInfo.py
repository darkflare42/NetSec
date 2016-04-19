import csv
Domain='Domain'
ns='Name Servers'
ws='Web Servers'
dns='DNS Servers'

headers=[Domain,ns, ws, dns]
writeToFile=csv.DictWriter(open('file3.csv','w'), delimiter=',',lineterminator='\n', fieldnames=headers)
writeToFile.writerow({Domain:Domain,ns:ns,ws:ws,dns : dns})

writeToFile.writerow({Domain:'Spam',ns:'hi',ws:'hhhh',dns :'sddsf'})
writeToFile.writerow({Domain:'Spam33',ns:'hi',ws:'hhhh',dns :'sddsf'})