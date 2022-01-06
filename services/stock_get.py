from model import Type
from .iservise import *


class StockGetService(IService):
    def run(self):
        types = self.get_all_types()
        return render_template('stock.html', types=types)

    @staticmethod
    def get_all_types():
        """ Получить все типы компонентов

        :return Список типов компонентов """
        return Type.select()
