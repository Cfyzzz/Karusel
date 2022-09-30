from playhouse.migrate import *

from settings import DATABASE


def run():
    base_path = DATABASE["path"]
    my_db = SqliteDatabase(base_path)
    migrator = SqliteMigrator(my_db)

    number = IntegerField(default=0)
    migrate(
        migrator.add_column('Karusel', 'number', number),
    )

    my_db.close()
