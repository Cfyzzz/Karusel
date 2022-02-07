from peewee import DoesNotExist

import tools
from model import Component, Type
from .iservise import *


class ComponentsGetService(IService):
    def run(self):
        query = self.get_rows(self.request.args)
        data = [item.serialize for item in query]
        if data:
            res = jsonify({
                'components': data
            })
            res.headers.add("Access-Control-Allow-Origin", "*")
            res.status_code = 200
        else:
            # if no results are found.
            output = {
                "error": "No results found. Check url again",
                "url": self.request.url,
            }
            res = jsonify(output)
            res.headers.add("Access-Control-Allow-Origin", "*")
            res.status_code = 404
        return res

    @staticmethod
    def get_rows(params: dict):
        """ Получить записи по фильтру
        Любые колмпоненты можно получить по следующим фильтрам: id, designation, address, box/
        Если не найдены компоненты, производится фильтра по полям type, value - в этом случае
        обязательны оба поля (используется для поиска резисторов и кондиционеров).

        :param params: фильтр для запроса"""
        try:
            if len(params) > 0:
                available_filter = ["id", "package", "designation", "address", "box"]
                filters = [getattr(Component, k) == v for k, v in params.items() if k in available_filter]
                if len(filters) > 0:
                    components = Component.select().where(*filters)

                    if len(components) > 0:
                        return components

                if "type" not in params or "value" not in params:
                    return []

                components = []
                value = tools.union_metric_format(params["value"])
                type_ = Type.get(Type.type == params["type"])
                all_components = Component.select().where(Component.type == type_)
                for component in all_components:
                    value_comp = tools.union_metric_format(component.designation)
                    if value_comp == value:
                        components.append(component)
                return components
            return Component.select()
        except DoesNotExist:
            return []
