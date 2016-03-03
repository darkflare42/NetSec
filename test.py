# this is a test
from NetModule import *

createDomainDict("www.yahoo.com")

def log(msg):
    print(msg)

print(get_authoritative_nameserver("www.yahoo.com", log))

print("===================")
print(query_authoritative_ns("www.yahoo.com", log))