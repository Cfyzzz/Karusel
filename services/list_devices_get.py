from model import Karusel
from .iservise import *


class ListDevicesGetService(IService):
    def run(self):
        karusels = Karusel.select()
        return render_template('devices.html', karusels=karusels)
