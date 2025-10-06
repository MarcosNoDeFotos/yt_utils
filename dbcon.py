import sqlite3

def getDB():
    return sqlite3.connect("database.db", timeout=5)

def getSequence(tabla):
    cursor = getDB().cursor()
    cursor.execute(f"select seq from sqlite_sequence where name = '{tabla}'")
    try:
        seq = cursor.fetchone()[0]+1
    except:
        seq = 1
    cursor.close()
    cursor.connection.close()
    return seq

sqlCursor = getDB().cursor()
sqlCursor.execute("CREATE TABLE if not exists config_sonidos(id integer primary key autoincrement, identificador varchar(200), rutaFichero varchar(2000))")
sqlCursor.execute("CREATE TABLE if not exists configuracion(id integer primary key autoincrement, salida_audio varchar(60), microfono_default varchar(60))")
db = getDB()
cursor = db.cursor()
try:
    cursor.execute("insert into configuracion(id) values(1)")
    db.commit()
except:
    None
cursor.close()
db.close()

sqlCursor.close()
sqlCursor.connection.close()