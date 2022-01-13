import tools
from .iservise import *


class ComponentsPushPutService(IService):
    def run(self):
        if not self.request.json:
            abort(400)

        if 'box' not in self.request.json or 'address' not in self.request.json:
            abort(400)

        _, created = self.append_component(self.request.json)
        res = jsonify({})
        res.status_code = 201 if created else 204
        return res

    @staticmethod
    def append_component(json_component: dict):
        """ Добавляет компонент в базу. Увеличивает счетчик, если такой существуюет, иначе создаёт новый

        :param json_component - словарь с полями компонента
        :return component, created - компонент и флаг о создании нового в базе
        """
        quantity = int(json_component.pop("quantity", 0))
        component, created = tools.new_component(json_component)
        if component is None:
            return None, None
        component.quantity += quantity
        component.save()
        return component, created
