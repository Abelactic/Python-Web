from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
from plots.graficasAD import (grafica_tipos, grafica_gen)

app = Flask(__name__)

# Rutas a archivos JSON y carpetas
USUARIOS_FILE = os.path.join(app.static_folder, 'json', 'usuarios.json')
REGISTROS_FILE = os.path.join(app.static_folder, 'json', 'registros.json')
PROYECTOS_FILE = os.path.join(app.static_folder, 'json', 'proyectos.json')
PROYECTOS_FOLDER = os.path.join(app.static_folder, 'proyectos')

# Crear carpeta de proyectos si no existe
if not os.path.exists(PROYECTOS_FOLDER):
    os.makedirs(PROYECTOS_FOLDER)

# Extensiones permitidas para imágenes y verificar que la imagenes cargadas son de este tipo
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
Funcion principal
Renderiza la pagina de inicio 
"""


@app.route('/', methods=['GET', 'POST'])
def inicio():

    return render_template('inicio.html')


"""
Funcion de inicio de sesion
Guarda el usuario y la contrasena en dos variables, despues las compara con lo
que se haya guardado en el archivo json llamado registros.json
Si el correo existe y la contrasena coincide entonces te permite entrar a la pagina
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if os.path.exists(USUARIOS_FILE):
            with open(USUARIOS_FILE, 'r') as f:
                usuarios = json.load(f)
            for user in usuarios:
                if user['email'] == email and user['password'] == password:
                    if user['rol'] == 1:
                        return redirect(url_for('admin'))
                    else:
                        return redirect(url_for('pagina1'))
        return render_template('inicio.html', mensaje_login='Credenciales incorrectas o usuario no encontrado.')

    return render_template('inicio.html')


"""
Funcion de registro
Guarda los datos de los nuevos usuarios en el archivo registro.json
Como cuando abres una cuenta nueva de facebook o roblox
"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('inicio.html', mensaje_register='Las contraseñas no coinciden.')

        if os.path.exists(USUARIOS_FILE):
            with open(USUARIOS_FILE, 'r') as f:
                usuarios = json.load(f)
        else:
            usuarios = []

        if any(u['email'] == email for u in usuarios):
            return render_template('login.html', mensaje_register='El correo ya está registrado.')

        usuarios.append({
            'nombre': nombre,
            'email': email,
            'password': password,
            'rol': 2
        })
        with open(USUARIOS_FILE, 'w') as f:
            json.dump(usuarios, f, indent=4)

        return redirect(url_for('pagina1'))

    return render_template('login.html')


"""
Funcion pagina 1
Renderiza la pagina de home
"""


@app.route('/pagina1')
def pagina1():
    return render_template('pagina1.html')


"""
Funcion para subir proyectos usando interfaz web
Esta funcion guarda los datos del proyecto como el nombre, un comentario y una foto
Esto para que la pagina web sirva como portafolio y muestren lo que hemos creado durante el curso
"""


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    mensaje = None

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')

        # Verificamos que se haya subido un archivo
        if 'imagen' not in request.files or request.files['imagen'].filename == '':
            mensaje = 'Por favor, selecciona una imagen.'
        else:
            file = request.files['imagen']

            if titulo and descripcion:

                filename = file.filename
                file_path = os.path.join(PROYECTOS_FOLDER, filename)
                file.save(file_path)

                # Cargamos o creamos la lista de proyectos
                if os.path.exists(PROYECTOS_FILE):
                    with open(PROYECTOS_FILE, 'r', encoding='utf-8') as f:
                        proyectos = json.load(f)
                else:
                    proyectos = []

                # Agregamos el nuevo proyecto
                proyectos.append({
                    'titulo': titulo,
                    'descripcion': descripcion,
                    'imagen_ruta': f'proyectos/{filename}'
                })

                # Guardamos el archivo JSON
                with open(PROYECTOS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(proyectos, f, indent=4, ensure_ascii=False)

                mensaje = '¡Proyecto subido exitosamente!'
            else:
                mensaje = 'Faltan el título o la descripción.'

    return render_template('admin.html', mensaje=mensaje)


"""
Funcion proyectos
Lee el archivo proyectos.json y acomoda la informacion en una pagina web para
que el publico las pueda observar
"""


@app.route('/proyectos')
def proyectos():
    if os.path.exists(PROYECTOS_FILE):
        with open(PROYECTOS_FILE, 'r') as f:
            proyectos = json.load(f)
    else:
        proyectos = []

    proyectos = proyectos[::-1]
    return render_template('galeria.html', proyectos=proyectos)


"""
Funcion analisis de datos
Renderiza las graficas que hemos realizado con analisis de datos en kaggle 
"""


@app.route('/pagina2')
def pagina2():
    img = grafica_tipos()
    gen = grafica_gen()
    return render_template('pagina2.html', img=img, gen=gen)


if __name__ == '__main__':
    app.run(debug=True)
