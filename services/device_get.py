from model import Karusel
from .iservise import *


class DeviceEditGetService(IService):
    def run(self):
        karusel_id = self.params.get('device_id', None)
        if karusel_id is None:
            return abort(404)

        karusel = Karusel.get_or_none(Karusel.id == karusel_id)
        if karusel:
            return render_template('device.html', karusel=karusel)
        return abort(404)
