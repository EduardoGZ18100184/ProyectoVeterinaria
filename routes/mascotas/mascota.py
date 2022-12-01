from flask import Blueprint, request,jsonify
from sqlalchemy import exc
from models import Mascota
from app import db,bcrypt
#from auth import tokenCheck

appmascota = Blueprint('appmascota',__name__,template_folder="templates")

@appmascota.route('/mascota/registro', methods =['POST'])
def registro():
    mascota  = request.get_json()
    mascotaExists = Mascota.query.filter_by(id=mascota['id']).first()
    print("buscando")
    print(mascota)
    print("imprimiento mascotaExists:")
    print(mascotaExists)
    
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
