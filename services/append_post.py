import json
import os

import requests
from flask import flash
from werkzeug.utils import redirect

import tools
from model import Component
from services.iservise import IService


class AppendPostService(IService):
    def run(self):
        base_url = tools.get_base_url()
        url = base_url + "/components/push"
        headers = {'Content-Type': 'application/json'}
        payload = {'type': self.request.form.get('type'),
                   'designation': self.request.form.get('designation'),
                   'description': self.request.form.get('description'),
                   'address': self.request.form.get('address'),
                   'box': self.request.form.get('box'),
                   'quantity': self.request.form.get('quantity'),
                   'min_amount': self.request.form.get('min_amount'),
                   'package': self.request.form.get('package'),
                   'datasheet': self.request.form.get('datasheet'),
                   }
        datasheet_new_file = self.request.files["file-new-datasheet"].filename
        try:
            resp = requests.put(url, headers=headers, data=json.dumps(payload, indent=4), timeout=15)
        except requests.exceptions.Timeout:
            flash("Сервис добавления нового компонента недоступен. Превышен интервал 15 cекунд")
            resp = None

        if datasheet_new_file:
            component = Component.get_by_id(resp.json()['id'])
            self.load_file("static/datasheets", component)
            url = base_url + "/components"
            payload = component.serialize
            try:
                resp2 = requests.post(url, headers=headers, data=json.dumps(payload, indent=4), timeout=15)
                if resp2.status_code != 201:
                    flash(f"Что-то пошло не так. Datasheet компонента {payload['type']} {payload['designation']} "
                          f"не записан")
            except requests.exceptions.Timeout:
                flash(f"Не получилось записать Datasheet компонента {payload['type']} {payload['designation']}"
                      f" по причине долгого ожидания (свыше 15 секунд). Можете открыть компонент в режиме "
                      f"редактирования и там добавить Datasheet")

        if resp and resp.status_code == 201:
            flash(f"Компонент {payload['type']} {payload['designation']} добавлен в количестве {payload['quantity']} шт.")
        elif resp and resp.status_code == 204:
            flash(f"Добавлен новый компонент {payload['type']} {payload['designation']} в количестве {payload['quantity']} шт.")
        else:
            flash("Что-то пошло не так. Компонент не добавлен")
        return redirect(self.request.url)

    def load_file(self, local_path, component: Component):
        file = self.request.files["file-new-datasheet"]
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
