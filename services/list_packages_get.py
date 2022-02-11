from model import Package, Type
from .iservise import *


class ListPackagesGetService(IService):
    def run(self):
        packages = self.get_all_packages()
        types = self.get_all_types()
        return render_template('packages.html', packages=packages, types=types)

    @staticmethod
    def get_all_packages():
        """ Получить все корпуса компонентов

        :return Список корпусов компонентов """
        return Package.select()

    @staticmethod
    def get_all_types():
        """ Получить все типы компонентов

        :return Список типов компонентов """
        return Type.select()
