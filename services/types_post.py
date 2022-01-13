import requests
from peewee import DoesNotExist

import tools
from model import Component
from .iservise import *


class TypesPostService(IService):
    def run(self):
        if self.request.form.get('componentOp') == "dec":
            url_pop = tools.get_base_url() + "/components/pop"
            payload_pop = {'id': self.request.form.get('componentId'), 'quantity': self.request.form.get('num')}
            headers = {'Content-Type': 'application/json'}
            requests.put(url_pop, headers=headers, data=json.dumps(payload_pop, indent=4))
            return redirect(request.url)

        elif self.request.form.get('componentOp') == "inc":
            try:
                component = Component.get_by_id(self.request.form.get('componentId'))
            except DoesNotExist:
                flash("Что-то пошло не так. Компонент не добавлен")
                return redirect(request.url)

            url = tools.get_base_url() + "/components/push"
            headers = {'Content-Type': 'application/json'}
            payload_push = {'id': component.id,
                            'quantity': self.request.form.get('num'),
                            'address': component.address,
                            'box': component.box,
                            'type': component.type.type
                            }
            requests.put(url, headers=headers, data=json.dumps(payload_push, indent=4))
            return redirect(request.url)

