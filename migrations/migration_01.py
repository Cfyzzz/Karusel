import os

from playhouse.migrate import *

from settings import DATABASE

base_path = os.path.join("..", DATABASE["path"])
my_db = SqliteDatabase(base_path)
migrator = SqliteMigrator(my_db)

min_amount_field = IntegerField(null=False, default=0)

migrate(
    migrator.add_column('Component', 'min_amount', min_amount_field),
)

my_db.close()
