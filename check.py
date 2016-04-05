import dns
import dns.message
import dns.query

def dd(IP_ADDRESS):
    try:
        queryCheck = dns.message.make_query('www.google.com', 2)
        print(dns.query.tcp(queryCheck,IP_ADDRESS,timeout=2))
    except dns.exception.Timeout:
        print("ff")




dd('37.203.95.199')