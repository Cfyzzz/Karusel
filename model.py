import peewee
from settings import DATABASE


database = peewee.SqliteDatabase(DATABASE["path"])


class Type(peewee.Model):
    type = peewee.CharField(max_length=64, null=False)

    class Meta:
        verbose_name = u"тип"
        verbose_name_plural = u"типы"
        database = database

    def __str__(self):
        return self.type

    def __repr__(self):
        return self.type


class Package(peewee.Model):
    package = peewee.CharField(max_length=16, null=False)
    type = peewee.ForeignKeyField(Type, null=False)

    class Meta:
        verbose_name = u"корпус"
        verbose_name_plural = u"корпуса"
        database = database

    def __str__(self):
        return self.package


class Karusel(peewee.Model):
    name = peewee.CharField(max_length=50, null=False)
    number = peewee.IntegerField(default=0)
    host = peewee.CharField(max_length=50, null=False, default='127.0.0.1')
    port = peewee.IntegerField(null=False, default=80)

    class Meta:
        verbose_name = u"карусель"
        verbose_name_plural = u"карусели"
        database = database


class Component(peewee.Model):
    type = peewee.ForeignKeyField(Type, null=False, on_delete='CASCADE')
    package = peewee.ForeignKeyField(Package, null=True, on_delete='CASCADE')
    designation = peewee.CharField(max_length=255, null=False)
    description = peewee.TextField(null=True)
    datasheet = peewee.TextField(null=True)
    address = peewee.CharField(max_length=8, null=False)
    box = peewee.CharField(max_length=4, null=False)
    quantity = peewee.IntegerField(null=False, default=0)
    min_amount = peewee.IntegerField(null=False, default=0)
    karusel = peewee.ForeignKeyField(Karusel, on_delete='CASCADE', null=True)

    class Meta:
        verbose_name = u"компонент"
        verbose_name_plural = u"компоненты"
        database = database

    @property
    def serialize(self):
        data = {
            'id': self.id,
            'type': str(self.type).strip(),
            'package': str(self.package).strip(),
            'designation': str(self.designation).strip(),
            'description': str(self.description),
            'datasheet': str(self.datasheet),
            'address': str(self.address).strip(),
            'box': str(self.box).strip(),
            'quantity': self.quantity,
            'karusel': str(self.karusel).strip(),
        }
        return data


def drop_all_tables():
    database.drop_tables([Type, Package, Component, Karusel])


def create_tables():
    database.create_tables([Type, Package, Component, Karusel])


database.connect()
create_tables()
