from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from sqlalchemy import exc
from models import Mascota
from app import db,bcrypt
from auth import tokenCheck, obtenerInfo
from models import User
from models import Cita
from flask_login import login_required

appcita = Blueprint('appcita',__name__,template_folder="templates")

#vista para registrar una mascota   #COMPLETADO
@appcita.route('/cita/registrar')
def func_add_cita_view():
    token = request.args.get('token')
    print("recibiendo token para verificar que el usuario no es admin y obtener el id")
    print(token)
    return render_template('agregarCitas.html', token = token) #render_template('appmascota.registro',token = token)

#registra una mascota               #SIGUE EN DESARROLLO
@appcita.route('/cita/registro', methods =['POST'])
def registro():
    token = request.form['token']
    print("recibiendo token para agendar la CITA")
    print(token)
    nombreMascota = request.form['nombre']
    fechaCita = request.form['fecha']

    usuario = obtenerInfo(token)
    info_user = usuario['data']
    idUsuario = info_user['user_id']
    IdMascotadb = db.engine.execute('select id from public."Mascotas" where user_id = ' + str(idUsuario) + ' and nombre = \'' + nombreMascota +'\';').first()
    
    if IdMascotadb is not None:
        mascotaId = IdMascotadb[0]
        print(mascotaId)
        cita = Cita(user_id = idUsuario, fecha = fechaCita, status = 'Agendada', mascota_id = mascotaId)
        try:
            db.session.add(cita)
            db.session.commit()
            mensaje="Cita creada"
        except exc.SQLAlchemyError as e:
            mensaje = "Error"
    else:
        mensaje="datos erroneos"  
        return (mensaje)   
    return (mensaje)   
    #return redirect(url_for('appsuer.func_user_view', auth_token=token))