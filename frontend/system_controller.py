import alsaaudio
import threading
from config import TEST_ENV
import pydbus

class SystemController():
    def __init__(self):
        self.system_volume = alsaaudio.Mixer().getvolume()[0]

    def get_volume(self):
        return self.system_volume

    def set_volume(self, vol):
        th = threading.Thread(target=self.__set_system_volume, args=(vol,))
        th.start()
        self.system_volume = vol

    def __set_system_volume(self, vol):
        m = alsaaudio.Mixer()
        m.setvolume(vol)


class Bluetoothctl():

    def __init__(self):

        self.bluez_service = 'org.bluez'
        self.adapter_path = '/org/bluez/hci0'

        self.bus = pydbus.SystemBus()
        self.adapter = self.bus.get(self.bluez_service, self.adapter_path)
        self.mngr = self.bus.get(self.bluez_service, '/')

    def get_paired_devices(self):
        mngd_objs = self.mngr.GetManagedObjects()
        paired_devices = []
        for path in mngd_objs:
            con_state = mngd_objs[path].get('org.bluez.Device1', {}).get('Paired', False)
            if con_state:
                addr = mngd_objs[path].get('org.bluez.Device1', {}).get('Address')
                name = mngd_objs[path].get('org.bluez.Device1', {}).get('Name')
                icon = mngd_objs[path].get('org.bluez.Device1', {}).get('Icon')
                print(mngd_objs[path].get('org.bluez.Device1', {}))
                paired_devices.append({'name': name, 'mac_address' : addr, 'icon' : icon})
        return paired_devices


    def connect(self, mac_address):
        device_path = f"{self.adapter_path}/dev_{mac_address.replace(':', '_')}"
        device = self.bus.get(self.bluez_service, device_path)
        connection_status = device.Connect()
        return connection_status
