from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,'src', 'templates')

app = Flask(__name__, template_folder=template_dir)

#Rutas de la app
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM vehiculo")
    myresult = cursor.fetchall()

    #convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar vehículos en base de datos
@app.route('/vehiculo', methods=['POST'])
def addVehiculos():
    placa = request.form['placa']
    marca = request.form['marca']
    modelo = request.form['modelo']
    fabricacion = request.form['fabricacion']
    color = request.form['color']
    fecha_ultimo_mantenimiento = request.form['fecha_ultimo_mantenimiento']
    kilometraje = request.form['kilometraje']
    precio_por_dia = request.form['precio_por_dia']
    estado = request.form['estado']
    sucursal = request.form['sucursal']

    if placa and marca and modelo and fabricacion and color and fecha_ultimo_mantenimiento and kilometraje and precio_por_dia and estado and sucursal:
        cursor = db.database.cursor()
        sql = "INSERT INTO vehiculo (placa, marca, modelo, fabricacion, color, fecha_ultimo_mantenimiento, kilometraje, precio_por_dia, estado, sucursal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (placa, marca, modelo, fabricacion, color, fecha_ultimo_mantenimiento, kilometraje, precio_por_dia, estado, sucursal )
        cursor.execute(sql, data)
        db.database.commit()

    return redirect(url_for('home'))


# Ruta para eliminar un vehículo
@app.route('/eliminar/<int:id_vehiculo>', methods=['POST'])
def eliminarVehiculo(id_vehiculo):
    # Eliminar el vehículo de la base de datos usando el ID
    cursor = db.database.cursor()
    sql = "DELETE FROM vehiculo WHERE Id_vehiculo = %s"
    cursor.execute(sql, (id_vehiculo,))
    db.database.commit()
    cursor.close()

    return redirect(url_for('home'))


@app.route('/editar/<int:id_vehiculo>', methods=['POST'])
def editar(id_vehiculo):
    placa = request.form['placa']
    marca = request.form['marca']
    modelo = request.form['modelo']
    fabricacion = request.form['fabricacion']
    color = request.form['color']
    fecha_ultimo_mantenimiento = request.form['fecha_ultimo_mantenimiento']
    kilometraje = request.form['kilometraje']
    precio_por_dia = request.form['precio_por_dia']
    estado = request.form['estado']
    sucursal = request.form['sucursal']

    if placa and marca and modelo and fabricacion and color and fecha_ultimo_mantenimiento and kilometraje and precio_por_dia and estado and sucursal:
        cursor = db.database.cursor()
        sql = "UPDATE vehiculo SET placa = %s, marca = %s, modelo = %s, fabricacion = %s, color = %s, fecha_ultimo_mantenimiento = %s, kilometraje = %s, precio_por_dia = %s, estado = %s, sucursal = %s WHERE id_vehiculo = %s"
        data = (placa, marca, modelo, fabricacion, color, fecha_ultimo_mantenimiento, kilometraje, precio_por_dia, estado, sucursal, id_vehiculo)
        cursor.execute(sql, data)
        db.database.commit()

    return redirect(url_for('home'))
           


if __name__ == '__main__':
    app.run(debug=True, port=4000)