from peewee import DoesNotExist

from model import Component
from .iservise import *


class ComponentsPopPutService(IService):
    def run(self):
        if not self.request.json:
            abort(400)

        result = self.decrement_component(self.request.json)
        if result is None:
            abort(400)

        res = jsonify({})
        res.status_code = 204
        return res

    @staticmethod
    def decrement_component(params: dict):
        """ Уменьшить количество [quantity] компонета [designation] по адресу [address, box]
        Обязательные поля: designation, address, box, quantity

        :param params - фильтр для запроса
        :returns результирующее количество компонента, иначе None
        """
        params_ = params.copy()
        try:
            available_filter = ["id", "package", "designation", "address", "box"]
            required_fields = ["designation", "address", "box", "quantity"]
            if all(map(lambda x: x in params_, required_fields)):
                quantity = params_.pop("quantity", 0)
                component = Component.get(
                    *[getattr(Component, k) == v for k, v in params_.items() if k in available_filter])
                component.quantity -= min(quantity, component.quantity)
                component.save()
            else:
                component = None
        except DoesNotExist:
            component = None

        if component:
            return component.quantity
        return component
