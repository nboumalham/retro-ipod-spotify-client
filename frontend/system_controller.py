import pulsectl
import threading
from config import TEST_ENV
import time
from config import logger
#import alsaaudio
import bluetooth


class SystemController():
    def __init__(self):
        self.system_volume = 100 #alsaaudio.Mixer().getvolume()[0]

    def get_volume(self):
        return self.system_volume

    def set_volume(self, vol):
        th = threading.Thread(target=self.__set_system_volume, args=(vol,))
        th.start()
        self.system_volume = vol

    def __set_system_volume(self, vol):
        #m = alsaaudio.Mixer()
        #m.setvolume(vol)
        self.m = 100


class Audioctl():
    def __init__(self):
        self.pulse = pulsectl.Pulse('my-client-name')

    def get_audio_output_devices(self):
        result = self.pulse.sink_list()
        output_devices = []
        for path in result:
            output_devices.append({'name': path.description, 'index' : path.index, 'connected' : True})
        return output_devices

    def select(self, device):
        result = self.pulse.sink_input_list()
        for path in result:
            self.pulse.sink_input_move(path.index ,device['index'])

class Bluetoothctl():

    def __init__(self):
        self.poop = "hello"

    
    def get_visible_devices(self):
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        devices = []
        for icon, addr, name, connected in nearby_devices:
            devices.append({'name': name, 'mac_address' : addr, 'icon' : 'low', 'connected' : False})
        return devices


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
                icon = mngd_objs[path].get('org.bluez.Device1', {}).get('Icon')
                connected = mngd_objs[path].get('org.bluez.Device1', {}).get('Connected')
                name = ('☑ ' if connected else '☐ ')  + mngd_objs[path].get('org.bluez.Device1', {}).get('Name')
                paired_devices.append({'name': name, 'mac_address' : addr, 'icon' : icon, 'connected' : connected})
        return paired_devices

    def toggle(self, device):
        if(device['connected']):
            logger.debug(device['name'] + " was connected. Disconnecting")
            return self.disconnect(device['mac_address'])
        else :
            logger.debug(device['name'] + " was disconnected. Connecting")
            return self.connect(device['mac_address'])

    def disconnect(self, mac_address):
        device_path = f"{self.adapter_path}/dev_{mac_address.replace(':', '_')}"
        device = self.bus.get(self.bluez_service, device_path)
        device.Disconnect()

    def connect(self, mac_address):
        device_path = f"{self.adapter_path}/dev_{mac_address.replace(':', '_')}"
        device = self.bus.get(self.bluez_service, device_path)
        device.Connect()