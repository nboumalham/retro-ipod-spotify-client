import alsaaudio
import threading
from config import TEST_ENV
import pydbus
import time

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

        self.connected_device = None

    def get_paired_devices(self):
        return self.get_devices('Paired')

    def get_connected_devices(self):
        return self.get_devices('Connected')

    def get_devices(self, filter):
        mngd_objs = self.mngr.GetManagedObjects()
        paired_devices = []
        for path in mngd_objs:
            con_state = mngd_objs[path].get('org.bluez.Device1', {}).get(filter, False)
            if con_state:
                addr = mngd_objs[path].get('org.bluez.Device1', {}).get('Address')
                icon = mngd_objs[path].get('org.bluez.Device1', {}).get('Icon')
                connected = mngd_objs[path].get('org.bluez.Device1', {}).get('Connected')
                name = ('[o] ' if connected else '[ ] ')  + mngd_objs[path].get('org.bluez.Device1', {}).get('Name')

                device_path = f"{self.adapter_path}/dev_{addr.replace(':', '_')}"
                device = self.bus.get(self.bluez_service, device_path)
                self.connected_device = device

                paired_devices.append({'name': name, 'mac_address' : addr, 'icon' : icon, 'connected' : connected})
        return paired_devices

    def toggle(self, device):
        if(device['connected']):
            print(device['name'] + " was connected. Disconnecting")
            return self.disconnect(device['mac_address'])
        else :
            print(device['name'] + " was disconnected. Connecting")
            return self.connect(device['mac_address'])

    def disconnect(self, mac_address):
        device_path = f"{self.adapter_path}/dev_{mac_address.replace(':', '_')}"
        device = self.bus.get(self.bluez_service, device_path)
        self.connected_device = None
        return self.connected_device

    def connect(self, mac_address):
        for connected_device in self.get_connected_devices():
            self.disconnect(connected_device['mac_address'])
        self.connected_device = None

        device_path = f"{self.adapter_path}/dev_{mac_address.replace(':', '_')}"
        device = self.bus.get(self.bluez_service, device_path)
        device.Connect()
        self.connected_device = device
        #print(device['name'] + " now connected")
        return self.connected_device
