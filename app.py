from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time


app = Flask(__name__)
CORS(app)


class Registro:

    def __init__(self, host, user, password, database):
        # conexion a la base
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # crea la base si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservas (
            id_reserva INT,
            nombre VARCHAR(45) NOT NULL,
            apellido VARCHAR(45) NOT NULL,
            mail VARCHAR(80) NOT NULL,
            fecha_ing DATE,
            fecha_egr DATE,
            habitacion VARCHAR(45) NOT NULL,            
            cantidad INT)
                            ''')
        self.conn.commit()

        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)


    def agregar_reserva (self, id_reserva, nombre, apellido, mail, fecha_ing, fecha_egr, habitacion, cantidad):
        # Verificamos si ya existe con el mismo código
        self.cursor.execute(f"SELECT * FROM reservas WHERE id_reserva = {id_reserva}")
        reserva_existe = self.cursor.fetchone()
        if reserva_existe:
            return False

        sql = "INSERT INTO reservas (id_reserva, nombre, apellido, mail, fecha_ing, fecha_egr, habitacion, cantidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (id_reserva, nombre, apellido, mail, fecha_ing, fecha_egr, habitacion, cantidad)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True

    def consultar_reserva(self, id_reserva):
        self.cursor.execute(f"SELECT * FROM reservas WHERE id_reserva = {id_reserva}")
        return self.cursor.fetchone()
    
    def modificar_reserva(self, id_reserva, nuevo_nombre, nuevo_apellido, nuevo_mail, nueva_fecha_ing, nueva_fecha_egr, nueva_habitacion, nueva_cantidad):
        sql = "UPDATE reservas SET nombre = %s, apellido = %s, mail = %s, fecha_ing = %s, fecha_egr = %s, habitacion = %s, cantidad = %s WHERE id_reserva = %s"
        datos = (nuevo_nombre, nuevo_apellido, nuevo_mail, nueva_fecha_ing, nueva_fecha_egr, nueva_habitacion, nueva_cantidad, id_reserva)
        self.cursor.execute(sql, datos)
        self.conn.commit()
        return self.cursor.rowcount > 0


    def listar_reservas(self):
        self.cursor.execute("SELECT * FROM reservas")
        reservas = self.cursor.fetchall()
        return reservas
    

    def eliminar_reserva(self, id_reserva):
        self.cursor.execute(f"DELETE FROM reservas WHERE id_reserva = {id_reserva}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    def mostrar_reserva(self, id_reserva):
        reserva = self.consultar_reserva(id_reserva)
        if reserva:
            print("-" * 40)
            print(f"Id.....: {reserva['id_reserva']}")
            print(f"Nombre: {reserva['nombre']}")
            print(f"Apellido...: {reserva['apellido']}")
            print(f"Mail.....: {reserva['mail']}")
            print(f"Fecha Ing.....: {reserva['fecha_ing']}")
            print(f"Fecha Egr..: {reserva['fecha_egr']}")
            print(f"Habitacion..: {reserva['habitacion']}")
            print(f"Huespedes..: {reserva['cantidad']}")
            print("-" * 40)
        else:
            print("Reserva no encontrada.")
    

    

#catalogo = Registro(host='localhost', user='root', password='', database='miapp')

catalogo = Registro(host='barbclavijo.mysql.pythonanywhere-services.com', user='barbclavijo', password='despegar23', database='barbclavijo$miapp')



@app.route('/reservas', methods=['GET'])
def listar_reservas():
    reservas = catalogo.listar_reservas()
    return jsonify(reservas)

@app.route("/reservas/<int:id_reserva>", methods=['GET'])
def mostrar_reserva(id_reserva):
    reserva = catalogo.consultar_reserva(id_reserva)
    if reserva:
        return jsonify(reserva), 201
    else:
        return "La reserva no existe", 404


@app.route('/reservas', methods=['POST'])
def agregar_reserva():
    #tomo los datos del form
    id_reserva = request.form['id_reserva']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    mail = request.form['mail']
    fecha_ing = request.form['fecha_ing']  
    fecha_egr = request.form['fecha_egr']
    habitacion = request.form['habitacion']
    cantidad = request.form['cantidad']

    reserva = catalogo.consultar_reserva(id_reserva)
        
    if catalogo.agregar_reserva(id_reserva, nombre, apellido, mail, fecha_ing, fecha_egr, habitacion, cantidad):
        return jsonify({"mensaje": "Reserva agregada"}), 201
    else:
        return jsonify({"mensaje": "La reserva ya existe"}), 400
    
@app.route("/reservas/<id_reserva>", methods=["DELETE"])
def eliminar_reserva(id_reserva):

    if catalogo.eliminar_reserva(id_reserva):
        return jsonify({"mensaje": "Producto eliminado"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar el producto"}), 500
    
@app.route("/reservas/<int:id_reserva>", methods=["PUT"])
def modificar_reserva(id_reserva):
    #Recojo los datos del form
    nuevo_nombre = request.form.get("nombre")
    nuevo_apellido = request.form.get("apellido")
    nuevo_mail = request.form.get("mail")
    nueva_fecha_ing = request.form.get("fecha_ing")
    nueva_fecha_egr = request.form.get("fecha_egr")
    nueva_habitacion = request.form.get("habitacion")
    nueva_cantidad = request.form.get("cantidad")

    #reserva = catalogo.consultar_reserva(id_reserva)

    if catalogo.modificar_reserva(id_reserva, nuevo_nombre, nuevo_apellido, nuevo_mail, nueva_fecha_ing, nueva_fecha_egr, nueva_habitacion, nueva_cantidad):
        return jsonify({"mensaje": "Reserva modificada"}), 200
    else:
        return jsonify({"mensaje": "Reserva no encontrada"}), 403

if __name__ == "__main__":
    app.run(debug=True)



