from peewee import DoesNotExist

import tools
from model import Component
from .iservise import *


class ComponentsPopPutService(IService):
    def run(self):
        if request.method == 'PUT':
            collect = self.request.json
        else:
            collect = self.request.args
        # if not self.request.json:
        if not collect:
            # abort(400)
            res = jsonify({})
            res.status_code = 400
            res.headers.add("Access-Control-Allow-Origin", "*")
            return res

        # result = self.decrement_component(self.request.json)
        result = self.decrement_component(collect)
        if result is None:
            # abort(400)
            res = jsonify({})
            res.status_code = 400
            res.headers.add("Access-Control-Allow-Origin", "*")
            return res

        res = jsonify({})
        res.status_code = 204
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res

    @staticmethod
    def decrement_component(params: dict):
        """ Уменьшить количество [quantity] компонета [designation] по адресу [address, box]
        Обязательные поля: designation, address, box, quantity

        :param params - фильтр для запроса
        :returns результирующее количество компонента, иначе None
        """
        params_ = params.copy()

        available_filter = ["id", "package", "designation", "address", "box"]
        required_fields = ["designation", "address", "box", "quantity"]
        if "id" in params_ or all(map(lambda x: x in params_, required_fields)):
            try:
                if "id" in params_:
                    component = Component.get_by_id(params_["id"])
                    if not tools.validate_component(component):
                        return None
                else:
                    component = Component.get(
                        *[getattr(Component, k) == v for k, v in params_.items() if k in available_filter])

                tools.prepare_data_component(params_, component.type)
                quantity = params_.pop("quantity", 0)
                if quantity > component.quantity:
                    flash(f"Недостаточное количество для списания компонента {component.type} {component.designation}")
                    return None
                component.quantity -= quantity
                component.save()
            except DoesNotExist:
                component = None
        else:
            component = None

        if component:
            return component.quantity
        return component
