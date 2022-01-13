import json

import requests
from flask import flash, url_for
from werkzeug.utils import redirect

import tools
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
                   'package': self.request.form.get('package'),
                   'datasheet': self.request.form.get('datasheet'),
                   }
        resp = requests.put(url, headers=headers, data=json.dumps(payload, indent=4))

        if resp.status_code == 201:
            flash(f"Компонент {payload['type']} {payload['designation']} добавлен в количестве {payload['quantity']} шт.")
        elif resp.status_code == 204:
            flash(f"Добавлен новый компонент {payload['type']} {payload['designation']} в количестве {payload['quantity']} шт.")
        else:
            flash("Что-то пошло не так. Компонент не добавлен")
        # return redirect(url_for('index'))
        return redirect(self.request.url)
