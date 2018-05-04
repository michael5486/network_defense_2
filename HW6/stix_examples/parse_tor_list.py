import re
from stix.core import STIXPackage
from stix.indicator import Indicator
from stix.ttp import TTP
from cybox.objects.address_object import Address

#used this file
#https://collector.torproject.org/recent/exit-lists/2018-05-04-19-02-00

def main():

    fileIn = open('tor_exit_node_list.txt', 'r')
    fileOut = open('tor_stix.xml', 'w')

    #print("List of Tor Exit nodes as of 5/4/2018")
    ip_addr_list = []

    for line in fileIn:

        ip_addr = re.search('(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))', line)
        if ip_addr:
            ip_addr_list.append(ip_addr)
            #print("    ", ip_addr.group(0))

    stix_package = STIXPackage()
    ttp = TTP(title="Tor Exit Nodes")

    i = 0
    for ip_addr in ip_addr_list:

        indicator = Indicator(title="IP Address for known Tor exit Node")
        indicator.add_indicator_type("IP Watchlist")
        addr = Address(address_value=ip_addr.group(0), category=Address.CAT_IPV4)
        addr.condition = "Equals"
        indicator.add_observable(addr)
        indicator.add_indicated_ttp(TTP(idref=ttp.id_))

        stix_package.add_indicator(indicator)
        print(i)
        i = i + 1

    stix_package.add_ttp(ttp)

    #print(stix_package.to_xml(encoding=None))
    fileOut.write(stix_package.to_xml(encoding=None))

if __name__ == '__main__':
    main()

