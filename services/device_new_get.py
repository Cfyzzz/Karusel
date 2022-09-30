from .iservise import *


class DeviceNewGetService(IService):
    def run(self):
        return render_template('device.html')
