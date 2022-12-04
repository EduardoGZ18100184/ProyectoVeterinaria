from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from sqlalchemy import exc
from models import Mascota
from app import db,bcrypt
from auth import tokenCheck, obtenerInfo
from models import User
from flask_login import login_required

appmascota = Blueprint('appmascota',__name__,template_folder="templates")

#vista para registrar una mascota   #COMPLETADO
@appmascota.route('/mascota/registrar')
def func_add_mascota_view():
    token = request.args.get('token')
    #token = request.args['auth_token']  # counterpart for url_for()
    print("recibiendo token para verificar que el usuario no es admin y obtener el id")
    print(token)
    return render_template('agregarMascotas.html', token = token) #render_template('appmascota.registro',token = token)

#registra una mascota               #COMPLETADO
@appmascota.route('/mascota/registro', methods =['POST'])
def registro():
    token = request.form['token']
    nombreMascota = request.form['nombre']
    tipoMascota = request.form['tipo']
    razaMascota = request.form['raza']
    usuario = obtenerInfo(token)
    info_user = usuario['data']
    maxIdMascotadb = db.engine.execute('select max(id) from public."Mascotas";').first()
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
    return redirect(url_for('appsuer.func_user_view', auth_token=token))

#Imprime todas las mascotas al recibir un token de usuario admin    #COMPLETADO
@appmascota.route('/mascotas') #get
def getAllPets():
    token = request.args.get('token')
    print(token)
    usuario = obtenerInfo(token)
    print(usuario)
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

#Imprime las mascotas por usuario       #COMPLETADO
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