import re
from stix.coa import CourseOfAction, Objective
from stix.common import Confidence
from stix.core import STIXPackage
from cybox.core import Observables
from cybox.objects.address_object import Address

#used this file
#https://collector.torproject.org/recent/exit-lists/2018-05-04-19-02-00

def main():

    fileIn = open('tor_exit_node_list.txt', 'r')
    fileOut = open('coa_tor.xml', 'w')

    #print("List of Tor Exit nodes as of 5/4/2018")
    ip_addr_list = []

    for line in fileIn:

        ip_addr = re.search('(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))', line)
        if ip_addr:
            ip_addr_list.append(ip_addr)
            #print("    ", ip_addr.group(0))

    pkg = STIXPackage()

    coa = CourseOfAction()
    coa.title = "Block traffic to Tor exit nodes"
    coa.stage = "Response"
    coa.type_ = "Perimeter Blocking"

    obj = Objective()
    obj.description = "Block communication to Tor exit nodes"
    obj.applicability_confidence = Confidence("High")

    i = 0
    observables_list = []
    for ip_addr in ip_addr_list:

        addr = Address(address_value=ip_addr.group(0), category=Address.CAT_IPV4)
        observables_list.append(addr)
        print(i)
        i = i + 1

    coa.parameter_observables = Observables(observables_list)
    pkg.add_course_of_action(coa)
    fileOut.write(pkg.to_xml(encoding=None))

if __name__ == '__main__':
    main()


