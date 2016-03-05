import socket
import dns.resolver #http://www.dnspython.org/
import dns
import dns.name
import dns.query



def createDomainDict(domain):
    domain_dict = {}
    getDomainIPS(domain, domain_dict)
    a = 5


def getDomainIPS(domain, dictionary):
    try:
        answers = dns.resolver.query(domain, "A") #ipv4
        for rdata in answers:
            dictionary["ipv4"] = rdata
        answers = dns.resolver.query(domain, "AAAA") #ipv6
        for rdata in answers:
            dictionary["ipv6"] = rdata
    except dns.resolver.NoAnswer:
        pass


def get_authoritative_nameserver(domain, log=lambda msg: None):
    n = dns.name.from_text(domain)

    depth = 2
    default = dns.resolver.get_default_resolver()
    nameserver = default.nameservers[0]

    last = False
    while not last:
        s = n.split(depth)

        last = s[0].to_unicode() == u'@'
        sub = s[1]

        log('Looking up %s on %s' % (sub, nameserver))
        query = dns.message.make_query(sub, dns.rdatatype.NS)
        response = dns.query.udp(query, nameserver)

        rcode = response.rcode()
        if rcode != dns.rcode.NOERROR:
            if rcode == dns.rcode.NXDOMAIN:
                raise Exception('%s does not exist.' % sub)
            else:
                raise Exception('Error %s' % dns.rcode.to_text(rcode))

        rrset = None
        if len(response.authority) > 0:
            rrset = response.authority[0]
        else:
            rrset = response.answer[0]

        rr = rrset[0]
        if rr.rdtype == dns.rdatatype.SOA:
            log('Same server is authoritative for %s' % sub)
        else:
            authority = rr.target
            log('%s is authoritative for %s' % (authority, sub))
            nameserver = default.query(authority).rrset[0].to_text()

        depth += 1

    return nameserver


def query_authoritative_ns (domain, log=lambda msg: None):

    default = dns.resolver.get_default_resolver()
    ns = default.nameservers[0]

    n = domain.split('.')

    for i in range(len(n), 0, -1):
        sub = '.'.join(n[i-1:])

        log('Looking up %s on %s' % (sub, ns))
        query = dns.message.make_query(sub, dns.rdatatype.NS)
        response = dns.query.udp(query, ns)

        rcode = response.rcode()
        if rcode != dns.rcode.NOERROR:
            if rcode == dns.rcode.NXDOMAIN:
                raise Exception('%s does not exist.' % (sub))
            else:
                raise Exception('Error %s' % (dns.rcode.to_text(rcode)))

        if len(response.authority) > 0:
            rrsets = response.authority
        elif len(response.additional) > 0:
            rrsets = [response.additional]
        else:
            rrsets = response.answer

        # Handle all RRsets, not just the first one
        for rrset in rrsets:
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.SOA:
                    log('Same server is authoritative for %s' % (sub))
                elif rr.rdtype == dns.rdatatype.A:
                    ns = rr.items[0].address
                    log('Glue record for %s: %s' % (rr.name, ns))
                elif rr.rdtype == dns.rdatatype.NS:
                    authority = rr.target
                    ns = default.query(authority).rrset[0].to_text()
                    log('%s [%s] is authoritative for %s; ttl %i' %
                        (authority, ns, sub, rrset.ttl))
                    result = rrset
                else:
                    # IPv6 glue records etc
                    #log('Ignoring %s' % (rr))
                    pass

    return result



