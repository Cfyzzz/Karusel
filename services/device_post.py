from peewee import DoesNotExist

from model import Karusel
from .iservise import *


class DeviceEditPostService(IService):
    def run(self):
        karusel_id = self.request.form.get('karuselId')
        if karusel_id:
            try:
                karusel = Karusel.get_by_id(karusel_id)
            except DoesNotExist:
                flash("Что-то пошло не так. Карусель не найдена")
                return redirect(request.url)

            host = self.request.form.get('host')
            port = self.request.form.get('port')
            if not (self.check_host(host) and self.check_port(port)):
                flash("Хост или порт указаны неправильно")
                return redirect(request.url)

            karusel.host = host
            karusel.port = port
            karusel.save()
            flash("Настройки карусели сохранены")
            print(request)
        return redirect(request.url)

    def check_host(self, host):
        return True

    def check_port(self, port):
        return True
