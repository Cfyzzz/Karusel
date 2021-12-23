from peewee import DoesNotExist

from model import Component
from .iservise import *


class ComponentsGetService(IService):
    def run(self):
        query = self.get_rows(self.request.args)
        data = [item.serialize for item in query]
        if data:
            res = jsonify({
                'components': data
            })
            res.status_code = 200
        else:
            # if no results are found.
            output = {
                "error": "No results found. Check url again",
                "url": self.request.url,
            }
            res = jsonify(output)
            res.status_code = 404
        return res

    @staticmethod
    def get_rows(params: dict) -> list[Component]:
        """ Получить записи по фильтру

        :param params: фильтр для запроса"""
        try:
            if len(params) > 0:
                available_filter = ["id", "package", "designation", "address", "box"]
                return Component.select().where(*[getattr(Component, k) == v for k, v in params.items()
                                                  if k in available_filter])
            return Component.select()
        except DoesNotExist:
            return []
