from flask import Blueprint, request,jsonify
from sqlalchemy import exc
from models import Mascota
from app import db,bcrypt
from auth import tokenCheck
from models import User
from flask_login import login_required

appmascota = Blueprint('appmascota',__name__,template_folder="templates")

#Imprime todas las mascotas si el token que recibe es de un usuario admin
@appmascota.route('/mascota/registro', methods =['POST'])
@login_required
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
@appmascota.route('/mascotas', methods=['POST'])
@tokenCheck
def getAllPets(usuario):
    print(usuario)
    print(usuario['admin'])
    if usuario['admin']:
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
        return jsonify({'mascotas':output})

#Imprime las mascotas por usuario al recibir un token
@appmascota.route('/mascotas-user', methods=['GET'])
@tokenCheck
def getMascotasUser(usuario):
    output = []
    id_usuario = usuario['user_id']
    mascotas = Mascota.query.filter_by(user_id=id_usuario)
    print(mascotas)
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
        output.append('El usuario no tiene mascotas')
    return jsonify({'mascotas':output})