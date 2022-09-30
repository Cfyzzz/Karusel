import re

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
        return redirect(request.url)

    @staticmethod
    def check_host(host):
        regexp = r'^([0-2]\d{,2}\.){3}[0-2]\d{,2}$'
        return re.match(regexp, host) is not None

    @staticmethod
    def check_port(port):
        regexp = r'^\d{2,4}$'
        return re.match(regexp, port) is not None
