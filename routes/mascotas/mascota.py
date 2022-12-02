from flask import Blueprint, request,jsonify
from sqlalchemy import exc
from models import Mascota
from app import db,bcrypt
from auth import tokenCheck

appmascota = Blueprint('appmascota',__name__,template_folder="templates")

@appmascota.route('/mascota/registro', methods =['POST'])
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


@appmascota.route('/mascotas', methods=['GET'])
@tokenCheck
def getUsers(usuario):
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