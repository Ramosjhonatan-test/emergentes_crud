from flask import Flask, redirect, request,url_for,render_template
import sqlite3

app = Flask(__name__)
#conexion alas base de dtaos
def get_db_connection():
    conn = sqlite3.connect('db_kardex.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS personal (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha_nac DATE NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
#creando la tabla
init_db()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personal')
def personal():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personal")
    personal = cursor.fetchall()
    return render_template('personal.html', personal = personal)  

@app.route('/personal/nuevo',methods=['GET', 'POST'])
def nuevo_personal():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        fecha_nac = request.form['fecha_nac']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO personal (nombre, telefono, fecha_nac) VALUES (?, ?, ?)",
                       (nombre, telefono, fecha_nac))
        conn.commit()
        conn.close()
        return redirect(url_for('personal'))
    return render_template('form_personal.html')

@app.route('/personal/eliminar/<int:id>', methods=['POST'])
def eliminar_personal(id):
    print(f"Intentando eliminar el registro con id: {id}")  # Depuración
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personal WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('personal'))

@app.route('/personal/editar/<int:id>', methods=['GET', 'POST'])
def editar_personal(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        fecha_nac = request.form['fecha_nac']

        # Actualizar el registro en la base de datos
        cursor.execute(
            "UPDATE personal SET nombre = ?, telefono = ?, fecha_nac = ? WHERE id = ?",
            (nombre, telefono, fecha_nac, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('personal'))
    else:
        # Obtener el registro actual para mostrarlo en el formulario
        cursor.execute("SELECT * FROM personal WHERE id = ?", (id,))
        personal = cursor.fetchone()
        conn.close()
        return render_template('form_personal.html', personal=personal)
    
if __name__ == '__main__':
    app.run(debug=True) 