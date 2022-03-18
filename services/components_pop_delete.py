from peewee import DoesNotExist

import tools
from model import Component
from .iservise import *


class ComponentsPopDeleteService(IService):
    def run(self):
        if self.delete_component(request.json):
            res = jsonify({})
            res.status_code = 204
        else:
            res = jsonify({
                "Error": "The requested resource is no longer available at the "
                         "server or incorrect parameters provided."
            })
            res.status_code = 410
        return res

    @staticmethod
    def delete_component(params: dict):
        """ Удалить компонент, соответствующий параметрам
        Обязательные поля: designation, address, box

        :param params - фильтр для запроса
        :returns количество удаленных строк в случае успеха, иначе None
        """
        try:
            available_filter = ["id", "package", "designation", "address", "box"]
            required_fields = ["designation", "address", "box"]
            if "id" in params or all(map(lambda x: x in params, required_fields)):
                if "id" in params:
                    component = Component.get_by_id(params["id"])
                    if not tools.validate_component(component):
                        component = None
                else:
                    component = Component.get(
                        *[getattr(Component, k) == v for k, v in params.items() if k in available_filter])
            else:
                component = None
        except DoesNotExist:
            component = None

        if component:
            return component.delete_instance()
        return component
