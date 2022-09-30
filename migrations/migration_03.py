from playhouse.migrate import *

from settings import DATABASE


def run():
    base_path = DATABASE["path"]
    my_db = SqliteDatabase(base_path)
    migrator = SqliteMigrator(my_db)

    host = CharField(max_length=50, null=False, default='127.000.000.001')
    port = IntegerField(null=False, default=80)

    migrate(
        migrator.add_column('Karusel', 'host', host),
        migrator.add_column('Karusel', 'port', port),
    )

    my_db.close()
