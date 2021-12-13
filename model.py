import peewee
from settings import DATABASE_NAME


database = peewee.SqliteDatabase(DATABASE_NAME)


class BaseTable(peewee.Model):
    # В подклассе Meta указываем подключение к той или иной базе данных
    class Meta:
        database = database


class Type(BaseTable):
    type = peewee.CharField(max_length=64, null=False)

    class Meta:
        verbose_name = u"тип"
        verbose_name_plural = u"типы"
        database = database

    def __str__(self):
        return self.type


class Package(BaseTable):
    package = peewee.CharField(max_length=16, null=False)

    class Meta:
        verbose_name = u"корпус"
        verbose_name_plural = u"корпуса"
        database = database


class Component(BaseTable):
    type = peewee.ForeignKeyField(Type, null=False)
    package = peewee.ForeignKeyField(Package, null=True)
    designation = peewee.CharField(max_length=255, null=False)
    description = peewee.TextField(null=True)
    datasheet = peewee.TextField(null=True)
    address = peewee.CharField(max_length=8, null=False)
    box = peewee.CharField(max_length=4, null=False)
    quantity = peewee.IntegerField(null=False, default=0)

    class Meta:
        verbose_name = u"компонент"
        verbose_name_plural = u"компоненты"
        database = database


def drop_all_tables():
    database.drop_tables([Type, Package, Component])


def create_tables():
    database.create_tables([Type, Package, Component])


database.connect()
create_tables()
