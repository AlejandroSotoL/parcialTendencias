import mysql.connector
from mysql.connector import Error

class Categoria:
    def __init__(self, categoria_id, nombre, descripcion):
        self.categoria_id = categoria_id
        self.nombre = nombre
        self.descripcion = descripcion

class Producto:
    def __init__(self, producto_id, nombre, descripcion, precio, stock):
        self.producto_id = producto_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

class ProductoCategoria:
    def __init__(self, producto_id, categoria_id):
        self.producto_id = producto_id
        self.categoria_id = categoria_id

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='parcial'
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def obtener_categoria(conexion, nombre):
    try:
        cursor = conexion.cursor()
        sql = "SELECT * FROM Categorias WHERE nombre = %s"
        cursor.execute(sql, (nombre,))
        categoria = cursor.fetchone()
        cursor.close()
        return categoria
    except Error as e:
        print("Error al buscar categoría:", e)
        return None

def listar_categorias(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Categorias")
        categorias = cursor.fetchall()
        cursor.close()
        return categorias
    except Error as e:
        print("Error al obtener categorías:", e)
        return []

def insertar_categoria():
    conexion = conectar_bd()
    if not conexion:
        return

    try:
        nombre = input("Ingrese el nombre de la categoría: ")
        categoria = obtener_categoria(conexion, nombre)

        if categoria:
            print(f"La categoría '{categoria[1]}' ya existe.")
            print("Seleccione una categoría de la lista:")
            categorias = listar_categorias(conexion)
            for cat in categorias:
                print(f"{cat[0]}. {cat[1]} - {cat[2]}")
            categoria_id = int(input("Ingrese el ID de la categoría a usar: "))
        else:
            descripcion = input("Ingrese la descripción de la categoría: ")
            cursor = conexion.cursor()
            sql = "INSERT INTO Categorias (nombre, descripcion) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, descripcion))
            categoria_id = cursor.lastrowid
            conexion.commit()
            cursor.close()
            print("Categoría insertada correctamente.")

        insertar_producto(categoria_id, conexion)
    except Error as e:
        print("Error al insertar categoría:", e)
    finally:
        conexion.close()

def insertar_producto(categoria_id, conexion):
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        nombre = input("Ingrese el nombre del producto: ")
        descripcion = input("Ingrese la descripción del producto: ")
        precio = float(input("Ingrese el precio del producto: "))
        stock = int(input("Ingrese el stock del producto: "))

        sql_producto = "INSERT INTO Productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_producto, (nombre, descripcion, precio, stock))
        producto_id = cursor.lastrowid

        sql_relacion = "INSERT INTO Productos_Categorias (producto_id, categoria_id) VALUES (%s, %s)"
        cursor.execute(sql_relacion, (producto_id, categoria_id))

        conexion.commit()
        print("Producto y relación con categoría insertados correctamente.")
    except Error as e:
        print("Error al insertar producto o relación:", e)
    finally:
        cursor.close()

def leer_todo():
    conexion = conectar_bd()
    if not conexion:
        return
    try:
        leer_categorias(conexion)
        leer_productos(conexion)
        leer_productos_categorias(conexion)
    finally:
        conexion.close()

def leer_categorias(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Categorias")
        categorias = cursor.fetchall()
        if categorias:
            print("\nCategorías:")
            for categoria in categorias:
                print(f"ID: {categoria[0]}, Nombre: {categoria[1]}, Descripción: {categoria[2]}")
        else:
            print("No hay categorías registradas.")
    except Error as e:
        print("Error al leer categorías:", e)
    finally:
        cursor.close()

def leer_productos(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        if productos:
            print("\nProductos:")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, "
                      f"Precio: {producto[3]}, Stock: {producto[4]}")
        else:
            print("No hay productos registrados.")
    except Error as e:
        print("Error al leer productos:", e)
    finally:
        cursor.close()

def leer_productos_categorias(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT p.nombre, c.nombre from productos P INNER JOIN productos_categorias pc on P.producto_id= pc.producto_id INNER JOIN categorias c on c.categoria_id= pc.categoria_id;")
        relaciones = cursor.fetchall()
        if relaciones:
            print("\nProductos-Categorías:")
            for relacion in relaciones:
                print(f"Producto: {relacion[0]}, Categoría: {relacion[1]}")
        else:
            print("No hay relaciones registradas en la tabla Productos_Categorias.")
    except Error as e:
        print("Error al leer la tabla Productos_Categorias:", e)
    finally:
        cursor.close()

if __name__ == "__main__":
    while True:
        print("\nMenú:")
        print("1. Insertar Categoría y Producto")
        print("2. Leer todos los registros")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case "1":
                insertar_categoria()
            case "2":
                leer_todo()
            case "3":
                print("Saliendo...")
                break
            case _:
                print("Opción no válida, intente de nuevo.")
