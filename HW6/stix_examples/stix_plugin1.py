from stix.core import STIXPackage
from stix.indicator import Indicator
from stix.ttp import TTP, Behavior
from stix.ttp.behavior import MalwareInstance
from cybox.core import Observable
from cybox.common import Hash
from cybox.objects.file_object import File
from cybox.objects.win_registry_key_object import WinRegistryKey
from cybox.objects.address_object import Address

def main():
    stix_package = STIXPackage()

    malware_instance = MalwareInstance()
    malware_instance.add_name("plugin1.exe")
    #not really remote access but am not sure what else to put
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
    file_plugin1.add_hash(Hash("ae768b62f5fef4dd604e1b736bdbc3ed30417ef4f67bff74bb57f779d794d6df"))
    file_plugin1.hashes[0].simple_hash_value.condition = "Equals"

    #observable 3 registry key
    #http://cybox.readthedocs.io/en/stable/api/coverage.html
    registry_object = WinRegistryKey()
    registry_object.name = "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\Google Ultron Updater"

    #observable 4 network traffic
    #http://stixproject.github.io/documentation/idioms/malware-hash/
    #I couldn't figure out how to correctly indicate the source, dest or protocol
    addr = Address(address_value="192.168.52.219", category=Address.CAT_IPV4)

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

    #indicator4 network traffic
    indicator4 = Indicator(title="Network Traffic for plugine1.exe")
    indicator.add_indicator_type("IP Watchlist")
    indicator4.add_observable(Observable(addr))
    indicator4.add_indicated_ttp(TTP(idref=ttp.id_))

    stix_package.add_indicator(indicator)
    stix_package.add_indicator(indicator2)
    stix_package.add_indicator(indicator3)
    stix_package.add_indicator(indicator4)
    stix_package.add_ttp(ttp)

    print(stix_package.to_xml(encoding=None))

if __name__ == '__main__':
    main()
