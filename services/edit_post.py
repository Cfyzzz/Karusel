import json
import os

import requests
from flask import flash
from peewee import DoesNotExist
from werkzeug.utils import redirect

import tools
from model import Component
from services.iservise import IService


class EditPostService(IService):
    def run(self):
        if self.request.form.get('componentId'):
            try:
                component = Component.get_by_id(self.request.form.get('componentId'))
            except DoesNotExist:
                flash("Что-то пошло не так. Компонент не найден")
                return redirect(self.request.url)
        else:
            flash("Что-то пошло не так. Компонент не найден")
            return redirect(self.request.url)

        if self.request.form.get('componentOp') == "load":
            self.load_file("static/datasheets", component)
            return redirect(self.request.url)

        base_url = tools.get_base_url()
        url = base_url + "/components"
        headers = {'Content-Type': 'application/json'}
        payload = {'type': self.request.form.get('type'),
                   'designation': self.request.form.get('designation'),
                   'description': self.request.form.get('description'),
                   'address': self.request.form.get('address'),
                   'box': self.request.form.get('box'),
                   'quantity': self.request.form.get('quantity'),
                   'package': self.request.form.get('package'),
                   'datasheet': self.request.form.get('datasheet'),
                   'id': component.id,
                   }
        resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

        if resp.status_code == 201:
            flash(
                f"Компонент {payload['type']} {payload['designation']} записан")
        else:
            flash("Что-то пошло не так. Компонент не записан")
        return redirect(self.request.url)

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
            return redirect(self.request.url)
        else:
            flash("Такой файл не является разрешенным. Разрешенные файлы: "
                  "'pdf', 'doc', 'docx', 'rtf', 'odt', 'txt', 'zip'")
        return redirect(self.request.url)

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in {'pdf', 'doc', 'docx', 'rtf', 'odt', 'txt', 'zip'}