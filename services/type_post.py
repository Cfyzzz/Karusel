import requests
from peewee import DoesNotExist

import tools
from model import Component
from .iservise import *


class TypePostService(IService):
    def run(self):
        if self.request.form.get('componentOp') == "dec":
            try:
                component = Component.get_by_id(self.request.form.get('componentId'))
            except DoesNotExist:
                flash("Что-то пошло не так. Компонент не найден")
                return redirect(request.url)

            url_pop = tools.get_base_url() + "/components/pop"
            payload_pop = {'id': self.request.form.get('componentId'), 'quantity': self.request.form.get('numDec')}
            headers = {'Content-Type': 'application/json'}
            requests.put(url_pop, headers=headers, data=json.dumps(payload_pop, indent=4))

            is_karusel = component.box.strip().lower()[0:1] in ["k", "к"]
            if is_karusel and self.request.form.get('openKarusel') == 'on':
                address = component.address.split("-")
                if len(address) == 2:
                    row_device = address[0].strip()
                    column_device = address[1].strip()
                    floor_device = component.box[1:].strip()
                    url = tools.get_url_karusel() \
                          + "/get?row=" + row_device \
                          + "&column=" + column_device \
                          + "&floor=" + floor_device
                    try:
                        requests.get(url, timeout=3)
                    except requests.exceptions.ConnectTimeout:
                        flash("На карусель запрос не ушёл :(")
        elif self.request.form.get('componentOp') == "inc":
            try:
                component = Component.get_by_id(self.request.form.get('componentId'))
            except DoesNotExist:
                flash("Что-то пошло не так. Компонент не добавлен")
                return redirect(request.url)

            url = tools.get_base_url() + "/components/push"
            headers = {'Content-Type': 'application/json'}
            payload_push = {'id': component.id,
                            'quantity': self.request.form.get('numInc'),
                            'address': component.address,
                            'box': component.box,
                            'type': component.type.type
                            }
            requests.put(url, headers=headers, data=json.dumps(payload_push, indent=4))
        return redirect(request.url)
