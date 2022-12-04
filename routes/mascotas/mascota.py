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

#registra una mascota
@appmascota.route('/mascota/registro', methods =['POST'])
def registro():
    print("dentro de registro")
    #mascota  = request.get_json()
    token = request.form['token']
    nombreMascota = request.form['nombre']
    tipoMascota = request.form['tipo']
    razaMascota = request.form['raza']
    #mascotaExists = Mascota.query.filter_by(id=mascota['id']).first()
    usuario = obtenerInfo(token)
    info_user = usuario['data']
    print("imprimiendo info user en /mascota/registro")
    #print(info_user)
    print(nombreMascota)
    #mascotaExists = info_user
    print("imprimiendo mascotaExists")
    print(info_user)

    #maxIdMascota = Mascota.query.all().first().orderby
    maxIdMascotadb = db.engine.execute('select max(id) from public."Mascotas";').first()
    print(maxIdMascotadb[0])
    print(type(maxIdMascotadb[0]))
    nuevoId = maxIdMascotadb[0] + 1
    if info_user:
        mascota = Mascota(id=nuevoId,nombre=nombreMascota,user_id=info_user["user_id"],raza=razaMascota,tipo=tipoMascota)
        try:
            db.session.add(mascota)
            db.session.commit()
            mensaje="Mascota creada"
        except exc.SQLAlchemyError as e:
            mensaje = "Error"
    else:
        mensaje="datos erroneos"     
    return jsonify({"message":mensaje})

# #registra una mascota
# @appmascota.route('/mascota/registro', methods =['POST'])
# #@login_required
# def registro():
#     mascota  = request.get_json()
#     mascotaExists = Mascota.query.filter_by(id=mascota['id']).first()
    
#     if not mascotaExists:
#         mascota = Mascota(id=mascota["id"],nombre=mascota["nombre"],user_id=mascota["user_id"],raza=mascota["raza"],tipo=mascota["tipo"])
#         try:
#             db.session.add(mascota)
#             db.session.commit()
#             mensaje="Mascota creada"
#         except exc.SQLAlchemyError as e:
#             mensaje = "Error"
#     else:
#         mensaje="Mascota existente"     
#     return jsonify({"message":mensaje})

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

#Imprime las mascotas por usuario
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