from flask import render_template, redirect, request, session, flash
from flask_app import app

#Importamos modelo
from flask_app.models.users import User
from flask_app.models.messages import Message

#Importación de Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    
        # Validamos la informacion que recibimos
    if not User.valida_usuario(request.form):
        return redirect('/')


    #Guardar registro
    pwd = bcrypt.generate_password_hash(request.form['password'])#Encriptando la contraseña del usuario y guardandola en pwd

    #Creamos un diccionario con todos los datos de request.form
    #  request.form['password'] = pwd --> ERROR: request.form NO se puede cambiar
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario) #Recibit el ID del nuevo usuario


    session['user_id'] = id # Guardamos en session el indentificador del usuario
    
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    #Verificamos que el email exista en la Base de datos
    user = User.get_by_email(request.form) #Recibimos una instancia de usuario O False

    if not user: #Si user = False / sino se cumple con esta funcion sigue con a sigiente y la siguiente y así
        flash('E-mail no encontrado', 'login')
        return redirect('/')

    #user es una instancia con todos los datos de mi usuario
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')

    session['user_id'] = user.id
    return redirect('/dashboard')


# @app.route('/welcome', methods=['POST'])
# def welcome():

#     session['first_name'] = request.form['frist_name']
#     return redirect ('/dashboard')




@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID


#  lista con todos los mensajes del ususario que recibio
    messages = Message.get_user_messages(formulario)

#  Lista con TODOS los usuarios
    users = User.get_all()
#contador mensajes
    mensajes = Message.get_count_mensajes(formulario)

    return render_template('dashboard.html', user=user, users=users, messages=messages, mensajes=mensajes)




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
