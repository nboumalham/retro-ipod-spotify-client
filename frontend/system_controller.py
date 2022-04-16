import pulsectl
import threading
from config import TEST_ENV
import time
from config import logger
#import alsaaudio
import dbus


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
        self.bus = dbus.SystemBus()
        self.bluez_service = 'org.bluez'
        self.adapter_path = '/org/bluez/hci0'

    def proxyobj(self, bus, path, interface):
        """ commodity to apply an interface to a proxy object """
        obj = self.bus.get_object('org.bluez', path)
        return dbus.Interface(obj, interface)


    def filter_by_addr(self, objects, addr):
        """ filters the objects based on their support
        for the specified interface """
        device_path = f"{self.adapter_path}/dev_{addr.replace(':', '_')}"
        result = []
        for obj in objects :
            if obj["path"] == device_path:
                result.append(obj)
        return result

    def filter_by_interface(self, objects, interface_name):
        """ filters the objects based on their support
        for the specified interface """
        result = []
        for path in objects.keys():
            interfaces = objects[path]
            for interface in interfaces.keys():
                if interface == interface_name:
                    result.append(path)
        return result

    def get_paired_devices(self):
        # we need a dbus object manager
        manager = self.proxyobj(self.bus, "/", "org.freedesktop.DBus.ObjectManager")
        objects = manager.GetManagedObjects()
        # once we get the objects we have to pick the bluetooth devices.
        # They support the org.bluez.Device1 interface
        devices = self.filter_by_interface(objects, "org.bluez.Device1")
        # now we are ready to get the informations we need
        
        bt_devices = []
        for device in devices:
            obj = self.proxyobj(self.bus, device, 'org.freedesktop.DBus.Properties')
                    
            connected = str(obj.Get("org.bluez.Device1", "Connected"))
            bt_devices.append({
                "name": ('☑ ' if connected else '☐ ') + str(obj.Get("org.bluez.Device1", "Name")),
                "addr": str(obj.Get("org.bluez.Device1", "Address")),
                "connected" : str(obj.Get("org.bluez.Device1", "Connected")),
                "icon" : str(obj.Get("org.bluez.Device1", "Icon"))
            }) 
        return bt_devices

    def dicover_devices(self, filter):
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        devices = []
        for addr, name in nearby_devices:
            devices.append({'name': name, 'mac_address' : addr, 'icon' : 'low', 'connected' : False})
        return devices


    def get_connected_devices(self):
        return self.get_devices('Connected')

    def toggle(self, device):
        if(device['connected']):
            logger.debug(device['name'] + " was connected. Disconnecting")
            return self.disconnect(device['addr'])
        else :
            logger.debug(device['name'] + " was disconnected. Connecting")
            return self.connect(device['addr'])

    def disconnect(self, addr):
        device_path = f"{self.adapter_path}/dev_{addr.replace(':', '_')}"
        adapter = dbus.Interface(self.bus.get_object("org.bluez", device_path), "org.bluez.Device1")
        adapter.Disconnect()

    def connect(self, addr):
        device_path = f"{self.adapter_path}/dev_{addr.replace(':', '_')}"
        adapter = dbus.Interface(
        self.bus.get_object("org.bluez", device_path), "org.bluez.Device1")
        adapter.Connect()