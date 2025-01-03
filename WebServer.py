import mariadb
from flask import Flask, render_template, redirect, request

app = Flask(__name__, template_folder='plantillas')
pin = 4

def connect_db(q):
    try:
        # Conexión a la base de datos
        with mariadb.connect(
            host="XXXXX", 
            user="XXXXXXX", 
            password="XXXXXX", 
            database="XXXXX"
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(q)
                result = cursor.fetchall()
                return result
    except mariadb.Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return []

@app.route("/")
def hello():
    # Consulta los últimos 6 registros de la base de datos
    data = connect_db('SELECT id, temperature, humidity, date FROM tempdata ORDER BY id DESC LIMIT 6;') 
    return render_template('index.html', result=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)
