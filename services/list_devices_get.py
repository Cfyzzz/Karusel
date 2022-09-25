from .iservise import *


class ListDevicesGetService(IService):
    def run(self):
        karusel = {'id': 1, 'name': "Основная карусель"}
        return render_template('devices.html', karusels=[karusel])
