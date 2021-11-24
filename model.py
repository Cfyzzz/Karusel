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


class Package(BaseTable):
    package = peewee.CharField(max_length=16, null=False)

    class Meta:
        verbose_name = u"корпус"
        verbose_name_plural = u"корпуса"
        database = database


class Component(BaseTable):
    type = peewee.ForeignKeyField(Type, null=False)
    package = peewee.ForeignKeyField(Package, null=False)
    designation = peewee.CharField(max_length=255, null=False)
    description = peewee.TextField(null=False)
    datasheet = peewee.TextField()
    address = peewee.CharField(max_length=8, null=False)
    quantity = peewee.IntegerField(null=False)

    class Meta:
        verbose_name = u"компонент"
        verbose_name_plural = u"компоненты"
        database = database


database.connect()
database.create_tables([Type, Package, Component])
