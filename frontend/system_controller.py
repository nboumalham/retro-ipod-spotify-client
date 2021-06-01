import alsaaudio


class SystemController():
    def __init__(self):
        self.system_volume = alsaaudio.Mixer().getvolume()[0]

    def get_volume(self):
        return self.system_volume
        
    def set_volume(self, vol):
        m = alsaaudio.Mixer()
        m.setvolume(vol)
        self.system_volume = vol
