from flask import Blueprint, request,jsonify, render_template
from sqlalchemy import exc
from models import User
from app import db,bcrypt
from auth import tokenCheck, obtenerInfo

appuser = Blueprint('appsuer',__name__,template_folder="templates")

#vista de registrar usuarios
@appuser.route('/auth/registro')
def registro_view():
    return render_template('registro.html')

#registra un nuevo usuario normal
@appuser.route('/auth/registro', methods =['POST'])
def registro():
    user  = request.get_json()
    userExists = User.query.filter_by(email=user['email']).first()
    if not userExists:
        usuario = User(email=user["email"],password=user["password"])
        try:
            db.session.add(usuario)
            db.session.commit()
            mensaje="Usuario creado"
        except exc.SQLAlchemyError as e:
            mensaje = "Error"
    else:
        mensaje="Usuario existente"     
    return jsonify({"message":mensaje})

#vista de login
@appuser.route('/auth/login')
def login_view():
    return render_template('login.html')

#muestra el listado correspondiente para el usuario
# si es admin, el listado completo
# si es normal solo el de sus mascotas
@appuser.route('/auth/login' , methods =['POST'])
def login():
    nombreUser = request.form['email']
    userPass = request.form['password'] 
    searchUser = User.query.filter_by(email = nombreUser).first()
    if searchUser:
        validation = bcrypt.check_password_hash(searchUser.password,userPass)
        if validation:
            auth_token = searchUser.encode_auth_token(user_id=searchUser.id)
            print(auth_token)
            if searchUser.admin:
                print("El usuario es admin")
                return render_template('funcionesAdmin.html',auth_token = auth_token)
            else:
                print("El usuario NO es admin")
                return render_template('funcionesUsuario.html',auth_token = auth_token)
    return render_template('401.html')

#Muestra todos los usuarios si recibe un token de usuario admin
# @appuser.route('/usuarios', methods=['GET'])
# @tokenCheck
# def getUsers(usuario):
#     print(usuario)
#     print(usuario['admin'])
#     if usuario['admin']:
#         output = []
#         usuarios = User.query.all()
#         for usuario in usuarios:
#             usuarioData = {}
#             usuarioData['id'] = usuario.id
#             usuarioData['email'] = usuario.email
#             usuarioData['password'] = usuario.password
#             usuarioData['registered_on'] = usuario.registered_on
#             usuarioData['admin'] = usuario.admin
#             output.append(usuarioData)
#         return jsonify({'usuarios':output})

# #Prueba de recibir un token e imprimir todos los usuarios
# @appuser.route('/pba-users', methods=['POST'])
# #@tokenCheck
# #@obtenerInfo
# def obtenerUsuarios():
#     token = request.form['token']
#     #print(token)
#     #tokenUser = User()
#     #print(usuario['admin'])
#     #tokenUser = obtenerInfo(token)
#     print("imprimiendo info del usuario desde /pba-users")
#     print(token)
#     usuario = obtenerInfo(token)
#     print(usuario)
#     ifo_user = usuario['data']
#     if ifo_user['admin']:
#         output = []
#         usuarios = User.query.all()
#         for usuario in usuarios:
#             usuarioData = {}
#             usuarioData['id'] = usuario.id
#             usuarioData['email'] = usuario.email
#             usuarioData['password'] = usuario.password
#             usuarioData['registered_on'] = usuario.registered_on
#             usuarioData['admin'] = usuario.admin
#             output.append(usuarioData)
#     return jsonify({'usuarios':output})

#Muestra todos los usuarios si recibe un token de usuario admin
@appuser.route('/usuarios')
def obtenerUsuarios():
    # if key doesn't exist, returns None
    token = request.args.get('token')
    usuario = obtenerInfo(token)
    info_user = usuario['data']
    if info_user['admin']:
        output = []
        usuarios = User.query.all()
        for usuario in usuarios:
            usuarioData = {}
            usuarioData['id'] = usuario.id
            usuarioData['email'] = usuario.email
            usuarioData['password'] = usuario.password
            usuarioData['registered_on'] = usuario.registered_on
            usuarioData['admin'] = usuario.admin
            output.append(usuarioData)
    print("imprimiendo info del usuario desde /usuarios")
    return jsonify({'usuarios':output})