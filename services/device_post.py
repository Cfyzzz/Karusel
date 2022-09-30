import re

from peewee import DoesNotExist

from model import Karusel
from .iservise import *


class DeviceEditPostService(IService):
    def run(self):
        karusel_id = int(self.request.form.get('karuselId', -1))
        operation = self.request.form.get('operation')
        if operation == 'save' and karusel_id > 0:
            try:
                karusel = Karusel.get_by_id(karusel_id)
            except DoesNotExist:
                flash("Что-то пошло не так. Карусель не найдена")
                return redirect(request.url)

            name = self.request.form.get('name')
            number = self.request.form.get('number')
            host = self.request.form.get('host')
            port = self.request.form.get('port')
            if not (self.check_host(host) and self.check_port(port)):
                flash("Хост или порт указаны неправильно")
                return redirect(request.url)

            karusel.name = name
            karusel.number = number
            karusel.host = host
            karusel.port = port
            karusel.save()
            flash("Настройки карусели сохранены")
        elif operation == 'save' and karusel_id == 0:
            name = self.request.form.get('name')
            number = self.request.form.get('number')
            host = self.request.form.get('host')
            port = self.request.form.get('port')
            if not (self.check_host(host) and self.check_port(port)):
                flash("Хост или порт указаны неправильно")
                return redirect(request.url)
            karusel = Karusel.create(
                name=name,
                number=number,
                host=host,
                port=port,
            )
            if karusel:
                flash("Настройки карусели сохранены")
            else:
                flash("Настройки карусели НЕ сохранены. Что-то пошло не так...")
        elif operation == 'delete' and karusel_id > 0:
            try:
                karusel = Karusel.get_by_id(karusel_id)
            except DoesNotExist:
                flash("Что-то пошло не так. Карусель не найдена")
                return redirect(request.url)
            if karusel:
                flash(f"Карусель '{karusel.name}' удалена")
                karusel.delete_instance()
                return redirect('/devices')
        return redirect('/devices/' + str(karusel.id))

    @staticmethod
    def check_host(host):
        regexp = r'^([0-2]\d{,2}\.){3}[0-2]\d{,2}$'
        return re.match(regexp, host) is not None

    @staticmethod
    def check_port(port):
        regexp = r'^\d{2,4}$'
        return re.match(regexp, port) is not None
