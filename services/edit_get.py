from peewee import DoesNotExist

from model import Component
from .iservise import *


class EditGetService(IService):
    def run(self):
        component_id = self.request.args.get('id', None)
        if component_id is None:
            return abort(404)

        component: Component = self.get_component(component_id)
        if component is None:
            return abort(404)

        return render_template('append.html',
                               types=[component.type],
                               packages=[component.package],
                               component=component
                               )

    @staticmethod
    def get_component(component_id: int) -> [Component, None]:
        """ Получить компонет согласно его id

        :param component_id - идентификатор id типа
        :return Component - компонент с id равным component_id или None
        """
        try:
            return Component.get_by_id(component_id)
        except DoesNotExist:
            return
