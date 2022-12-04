from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import exc
from models import Mascota
from app import db,bcrypt
from auth import tokenCheck, obtenerInfo
from models import User
from flask_login import login_required

appmascota = Blueprint('appmascota',__name__,template_folder="templates")

#vista para registrar una mascota
@appmascota.route('/mascota/registrar')
def func_add_mascota_view():
    token = request.args.get('token')
    #token = request.args['auth_token']  # counterpart for url_for()
    print("recibiendo token para verificar que el usuario no es admin y obtener el id")
    print(token)
    return render_template('agregarMascotas.html', token = token) #render_template('appmascota.registro',token = token)

#Imprime todas las mascotas si el token que recibe es de un usuario admin
@appmascota.route('/mascota/registro', methods =['POST'])
#@login_required
def registro():
    mascota  = request.get_json()
    mascotaExists = Mascota.query.filter_by(id=mascota['id']).first()
    
    if not mascotaExists:
        mascota = Mascota(id=mascota["id"],nombre=mascota["nombre"],user_id=mascota["user_id"],raza=mascota["raza"],tipo=mascota["tipo"])
        try:
            db.session.add(mascota)
            db.session.commit()
            mensaje="Mascota creada"
        except exc.SQLAlchemyError as e:
            mensaje = "Error"
    else:
        mensaje="Mascota existente"     
    return jsonify({"message":mensaje})

#Imprime todas las mascotas al recibir un token de usuario admin
#@appmascota.route('/mascotas/<token>', methods=['GET'])
# @appmascota.route('/mascotas', methods=['POST'])
# @tokenCheck
# def getAllPets(usuario):
#     print(usuario)
#     print(usuario['admin'])
#     if usuario['admin']:
#         output = []
#         mascotas = Mascota.query.all()
#         for mascota in mascotas:
#             mascotaData = {}
#             mascotaData['id'] = mascota.id
#             mascotaData['nombre'] = mascota.nombre
#             mascotaData['id_duenio'] = mascota.user_id
#             mascotaData['raza'] = mascota.raza
#             mascotaData['tipo'] = mascota.tipo
#             output.append(mascotaData)
#         return jsonify({'mascotas':output})

#Imprime todas las mascotas al recibir un token de usuario admin
@appmascota.route('/mascotas') #get
def getAllPets():
    token = request.args.get('token')
    usuario = obtenerInfo(token)
    info_user = usuario['data']
    if info_user['admin']:
        output = []
        mascotas = Mascota.query.all()
        for mascota in mascotas:
            mascotaData = {}
            mascotaData['id'] = mascota.id
            mascotaData['nombre'] = mascota.nombre
            mascotaData['id_duenio'] = mascota.user_id
            mascotaData['raza'] = mascota.raza
            mascotaData['tipo'] = mascota.tipo
            output.append(mascotaData)
    else:
        output.append('El usuario no es administrador')
    print("imprimiendo info del usuario desde /usuarios")
    return jsonify({'mascotas':output})

# #Imprime las mascotas por usuario al recibir un token
# @appmascota.route('/mascotas-user', methods=['GET'])
# @tokenCheck
# def getMascotasUser(usuario):
#     output = []
#     id_usuario = usuario['user_id']
#     mascotas = Mascota.query.filter_by(user_id=id_usuario)
#     print(mascotas)
#     if mascotas is not None:
#         for mascota in mascotas:
#             mascotaData = {}
#             mascotaData['id'] = mascota.id
#             mascotaData['nombre'] = mascota.nombre
#             mascotaData['id_duenio'] = mascota.user_id
#             mascotaData['raza'] = mascota.raza
#             mascotaData['tipo'] = mascota.tipo
#             output.append(mascotaData)
#     else:
#         output.append('El usuario no tiene mascotas')
#     return jsonify({'mascotas':output})

@appmascota.route('/mascotas-user') #get
def getMascotasUser():
    token = request.args.get('token')
    usuario = obtenerInfo(token)
    info_user = usuario['data']
    print(info_user)
    print(type(info_user))
    mascotas = Mascota.query.filter_by(user_id=info_user['user_id'])
    print(mascotas)
    output = []
    if mascotas is not None:
        for mascota in mascotas:
            mascotaData = {}
            mascotaData['id'] = mascota.id
            mascotaData['nombre'] = mascota.nombre
            mascotaData['id_duenio'] = mascota.user_id
            mascotaData['raza'] = mascota.raza
            mascotaData['tipo'] = mascota.tipo
            output.append(mascotaData)
    else:
        output.append('El usuario no es administrador')
    print("imprimiendo info del usuario desde /usuarios")
    return jsonify({'mascotas':output})

#registra una mascota
# @appmascota.route('/mascota/registro', methods =['POST'])
# def registro():
#     nombreUser = request.form['email']
#     userPass = request.form['password'] 
#     searchUser = User.query.filter_by(email = nombreUser).first()
#     if searchUser:
#         mensaje="Usuario existente"
#     else:
#         usuario = User(email=nombreUser,password=userPass)
#         try:
#             db.session.add(usuario)
#             db.session.commit()
#             mensaje="Usuario creado"
#         except exc.SQLAlchemyError as e:
#             mensaje = "Error" 
#     #return jsonify({"message":mensaje})
#     return render_template('msjLogin.html',mensaje = mensaje)