from playhouse.migrate import *

from settings import DATABASE


def run():
    base_path = DATABASE["path"]
    my_db = SqliteDatabase(base_path)
    migrator = SqliteMigrator(my_db)

    class Karusel(Model):
        name = CharField(max_length=50, null=False)

        class Meta:
            verbose_name = u"карусель"
            verbose_name_plural = u"карусели"
            database = my_db

    with my_db.transaction():
        Karusel.create_table()
        Karusel.create(name='Основная карусель')
        karusel = ForeignKeyField(Karusel, field=Karusel.id, on_delete='CASCADE', null=True)
        migrate(
            migrator.add_column('Component', 'karusel_id', karusel),
        )
    my_db.close()

    from model import Component
    for component in Component.select():
        component.karusel_id = 1
        component.save()
