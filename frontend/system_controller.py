import alsaaudio
import threading

class SystemController():
    def __init__(self):
        self.system_volume = alsaaudio.Mixer().getvolume()[0]

    def get_volume(self):
        return self.system_volume

    def set_volume(self, vol):
        th = threading.Thread(target=self.__set_system_volume, args=(vol,))
        th.start()

    def __set_system_volume(self, vol):
        m = alsaaudio.Mixer()
        m.setvolume(vol)
