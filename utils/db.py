import sqlite3
try:
    sqlite_connection = sqlite3.connect('hosting.db')
    cursor = sqlite_connection.cursor()
    print("База данных создана и успешно подключена к SQLite")

    sqlite_create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT);
    '''

    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()

    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)