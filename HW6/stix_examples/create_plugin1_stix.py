from stix.core import STIXPackage
from stix.indicator import Indicator
from stix.ttp import TTP, Behavior
from stix.ttp.behavior import MalwareInstance
from cybox.core import Observable
from cybox.objects.file_object import File
from cybox.objects.win_registry_key_object import WinRegistryKey
from cybox.objects.network_packet_object import NetworkPacket, IPv4Packet, IPv4Header
from cybox.common import Hash
from cybox.objects.address_object import Address

def main():
    stix_package = STIXPackage()

    malware_instance = MalwareInstance()
    malware_instance.add_name("plugin1.exe")
    #not really remote access but idk what else to put
    malware_instance.add_type("Remote Access Trojan")

    ttp = TTP(title="Install+plugin1.exe")
    ttp.behavior = Behavior()
    ttp.behavior.add_malware_instance(malware_instance)

    #observable 1 Install+plugin1.exe
    file_object = File()
    file_object.file_name = "Install+plugin1.exe"
    file_object.add_hash(Hash("164ecfc36893ee368a3c4cb2fd500b58262f1b87de1e68df74390db0b5445915"))
    file_object.hashes[0].simple_hash_value.condition = "Equals"

    #observable 2 plugin1.exe
    #http://cybox.readthedocs.io/en/stable/examples.html#creating-observables
    file_plugin1 = File()
    file_plugin1.file_name = "plugin1.exe"
    file_plugin1.file_path = "C:\\Users\\Default\\AppData\\Local\\temp\plugin1"
    file_plugin1.add_hash(Hash("insert Hash here"))
    file_plugin1.hashes[0].simple_hash_value.condition = "Equals"

    #observable 3 registry key
    #http://cybox.readthedocs.io/en/stable/api/coverage.html
    registry_object = WinRegistryKey()
    registry_object.name = "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\Google Ultron Updater"

    #observable 4 network traffic
    #http://cybox.readthedocs.io/en/stable/api/cybox/objects/network_packet_object.html#cybox.objects.network_packet_object.IPv4Header
    #http://cybox.readthedocs.io/en/stable/api/cybox/objects/address_object.html#cybox.objects.address_object.Address
    src_address = Address("192.168.52.2")
    dest_address = Address("192.168.52.2")
    nbns_ipv4_header = IPv4Header()
    nbns_ipv4_header.src_ipv4_addr = src_address
    nbns_ipv4_header.dest_ipv4_addr = dest_address
    #nbns.protocol = "NBNS"

    network_nbns_packet = IPv4Packet()
    network_nbns_packet.ipv4_header = nbns_ipv4_header


    #indicator 1 Install+plugin1.exe
    indicator = Indicator(title="File hash for Install+plugin.exe")
    indicator.add_indicator_type("File Hash Watchlist")
    indicator.add_observable(file_object)
    indicator.add_indicated_ttp(TTP(idref=ttp.id_))

    #indicator 2 plugin1.exe
    indicator2 = Indicator(title="File hash for plugin1.exe")
    indicator2.add_indicator_type("File Hash Watchlist")
    indicator2.add_observable(file_plugin1)
    indicator2.add_indicated_ttp(TTP(idref=ttp.id_))

    #indicator3 registry key
    indicator3 = Indicator(title="Registry entry for Install+plugin.exe")
    indicator3.add_indicator_type("Malware Artifacts")
    indicator3.add_observable(registry_object)
    indicator3.add_indicated_ttp(TTP(idref=ttp.id_))

    #indicator4 NBNS packet
    #use this to find sample code
    indicator4 = Indicator(title="NetBios network traffic")
    indicator4.add_indicator_type("IP Watchlist")
    indicator4.add_observable(nbns_ipv4_header)
    indicator4.add_indicated_ttp(TTP(idref=ttp.id_))

    stix_package.add_indicator(indicator)
    stix_package.add_indicator(indicator2)
    stix_package.add_indicator(indicator3)
    stix_package.add_ttp(ttp)

    print(stix_package.to_xml(encoding=None))

if __name__ == '__main__':
    main()



