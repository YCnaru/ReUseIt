from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Guarda la base de datos DENTRO de /instance/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reuseperu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Inicializa la base de datos
db = SQLAlchemy(app)
# Creación de una tabla


class Objeto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)  # articulo
    descripcion = db.Column(db.Text, nullable=False)  # descripción
    contacto = db.Column(db.String(100), nullable=False)  # contacto
    imagen = db.Column(db.String(200))  # imagen del archivo
    # Usuario que publica el objeto,


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable=False)  # nombre
    password = db.Column(db.String(30), nullable=False)  # contraseña


# Ruta para el inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']  # campo 'email'
            form_password = request.form['password']  # campo 'password'
            users_db = User.query.all()
            for user in users_db:
                if form_login == user.login and form_password == user.password:
                    return redirect('/index')
            else:
                error = 'Nombre de usuario o contraseña incorrectos'
                return render_template('login.html', error=error)
        else:
            return render_template('login.html')


# Ruta para el registro de usuarios
@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']
        user = User(login=login, password=password)

        db.session.add(user)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('register.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')


@app.route('/detalle')
def detalle():
    return render_template('detalle.html')


@app.route('/publicar', methods=['GET', 'POST'])
def publicar():
    if request.method == 'POST':
        nombre = request.form['nombre']  # Nombre del objeto
        descripcion = request.form['descripcion']  # Descripción del objeto
        contacto = request.form['contacto']   # Información de contacto
        imagen = request.form['imagen']  # URL de la imagen

        nuevo_objeto = Objeto(
            nombre=nombre,
            descripcion=descripcion,
            contacto=contacto,
            imagen=imagen,
            #Debe ir el nombre del usuario que publica
        )
        db.session.add(nuevo_objeto)
        db.session.commit()
        return redirect('/catalogo')  # Redireccionar al catálogo
    return render_template('publicar.html')


# Hacer que el usuario pueda eliminar su publicación


if __name__ == '__main__':
    app.run(debug=True)
