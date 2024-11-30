import dbcon

tabla = "config_sonidos"

class ConfigSonidos:
    def __init__(self, id, identificador, rutaFichero):
        self.id = id
        self.identificador = identificador
        self.rutaFichero = rutaFichero

def getConfiguracionesSonidos():
    configuraciones = []
    db = dbcon.getDB()
    cursor = db.cursor()
    results = cursor.execute(f"select id, identificador, rutaFichero from {tabla}")
    for r in results:
        configuraciones.append(ConfigSonidos(r[0], r[1], r[2]))
    cursor.close()
    db.close()
    return configuraciones

def nuevaConfiguracionSonido(identificador, rutaFichero):
    db = dbcon.getDB()
    cursor = db.cursor()
    result = cursor.execute(f"insert into {tabla}(identificador, rutaFichero) values(?,?)", (identificador, rutaFichero))
    db.commit()
    cursor.close()
    db.close()
    return result.rowcount == 1

def eliminarConfiguracionSonido(id):
    db = dbcon.getDB()
    cursor = db.cursor()
    result = cursor.execute(f"delete from {tabla} where id = ?", (id,))
    db.commit()
    cursor.close()
    db.close()
    return result.rowcount == 1

def actualizarConfiguracionSonido(id, identificador, rutaFichero):
    db = dbcon.getDB()
    cursor = db.cursor()
    result = cursor.execute(f"update {tabla} set identificador = ?, rutaFichero = ? where id = ?", (identificador, rutaFichero, id))
    db.commit()
    cursor.close()
    db.close()
    return result.rowcount == 1
