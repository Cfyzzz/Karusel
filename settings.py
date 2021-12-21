# configure our database
SECRET_KEY = 'ssshhhh'
DATABASE = {
    'name': 'components.sqlite3',
    'engine': 'peewee.SqliteDatabase',
    'user': 'username',
    'password': 'password',
    'host': 'localhost',
    'port': 3000,
}
