from model import Type, Component
from .iservise import *
from peewee import DoesNotExist


class TypesGetService(IService):
    def run(self):
        type_id = self.params.get('type_id', None)
        if type_id is None:
            return abort(404)

        components = self.get_components(type_id)
        type_component = self.get_type_by_id(type_id)
        return render_template('components.html', components=components, type_comp=type_component)

    @staticmethod
    def get_components(type_id: int):
        """ Получить компонеты согласно id типу

        :param type_id - идентификатор id типа
        """
        try:
            type_comp = Type.get_by_id(type_id)
            return Component.select().where(Component.type == type_comp)
        except DoesNotExist:
            return []

    @staticmethod
    def get_type_by_id(type_id: int):
        return Type.get_or_none(Type.id == type_id)
