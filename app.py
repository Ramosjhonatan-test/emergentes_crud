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

if __name__ == '__main__':
    app.run(debug=True) 