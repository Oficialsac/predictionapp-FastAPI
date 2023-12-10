import json 

db_path = 'auth/fakedb.json'

def read_file() -> dict:
    """
    Lee los datos del archivo de base de datos.

    Returns:
    - dict: Devuelve un diccionario con los datos de la base de datos.
    """
    with open(db_path) as db_file:
        db = json.load(db_file)
    return db

def write_file(data: dict) -> bool:
    """
    Escribe los datos en el archivo de base de datos.

    Parameters:
    - `data` (dict): Datos a escribir en el archivo.

    Returns:
    - bool: Devuelve True si la escritura es exitosa.
    """
    with open(db_path, 'w') as db_file:
        json.dump(data, db_file)
    
    return True
