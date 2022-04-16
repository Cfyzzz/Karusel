import os

import requests
from peewee import DoesNotExist

import tools
from model import Component
from .iservise import *


class TypePostService(IService):
    def run(self):
        headers = {'Content-Type': 'application/json'}
        if self.request.form.get('componentId'):
            try:
                component = Component.get_by_id(self.request.form.get('componentId'))
            except DoesNotExist:
                flash("Что-то пошло не так. Компонент не найден")
                return redirect(request.url)

        if self.request.form.get('componentOp') == "dec":
            url_pop = tools.get_base_url() + "/components/pop"
            payload_pop = {'id': self.request.form.get('componentId'), 'quantity': self.request.form.get('numDec')}
            requests.put(url_pop, headers=headers, data=json.dumps(payload_pop, indent=4))
            self.open_karusel(component)
        elif self.request.form.get('componentOp') == "inc":
            url = tools.get_base_url() + "/components/push"
            payload_push = {'id': component.id,
                            'quantity': self.request.form.get('numInc'),
                            'address': component.address,
                            'box': component.box,
                            'type': component.type.type
                            }
            requests.put(url, headers=headers, data=json.dumps(payload_push, indent=4))
            self.open_karusel(component)
        elif self.request.form.get('componentOp') == "delete":
            url_pop = tools.get_base_url() + "/components/pop"
            payload_pop = {'id': self.request.form.get('componentId')}
            requests.delete(url_pop, headers=headers, data=json.dumps(payload_pop, indent=4))
        elif self.request.form.get('componentOp') == "load":
            self.load_file("static/datasheets", component)
        return redirect(request.url)

    @staticmethod
    def open_karusel(component):
        is_karusel = component.box.strip().lower()[0:1] in ["k", "к"]
        if is_karusel:
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

    def load_file(self, local_path, component: Component):
        file = self.request.files["file"]
        if not os.access(local_path, os.F_OK):
            os.makedirs(local_path)
        if file and self.allowed_file(file.filename):
            path = os.path.join(local_path, file.filename)
            file.save(path)
            path = os.path.join(tools.get_base_url(), path)
            component.datasheet = path
            component.save()
            return redirect(request.url)
        # Что-то пошло не так...
        return redirect(request.url)

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in {'pdf', 'doc', 'docx', 'rtf', 'odt', 'txt'}
