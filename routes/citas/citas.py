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

#registra una mascota               #SIGUE EN DESARROLLO (Pendiente validaciones)
@appcita.route('/cita/registro', methods =['POST'])
def registro():
    token = request.form['token']
    print("recibiendo token para agendar la CITA")
    print(token)
    nombreMascota = request.form['nombre']
    fechaCita = request.form['fecha']
    if nombreMascota == '':
        mensaje = "Datos invalidos"
        return render_template('agregarCitas.html', token = token, mensaje = mensaje)
    
    usuario = obtenerInfo(token)
    info_user = usuario['data']
    idUsuario = info_user['user_id']
    IdMascotadb = db.engine.execute('select id from public."Mascotas" where user_id = ' + str(idUsuario) + ' and nombre = \'' + nombreMascota +'\';').first()
    #Validando que no exista otra cita con esa misma fecha
    searchDate = Cita.query.filter_by(fecha = fechaCita).first()
    if searchDate:
        mensaje="Horario no disponible"
        return render_template('agregarCitas.html', token = token, mensaje = mensaje)
        #return (mensaje)
    
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
        #return (mensaje)   
    return render_template('agregarCitas.html', token = token, mensaje = mensaje)
    #return (mensaje)   
    #return redirect(url_for('appsuer.func_user_view', auth_token=token))

#Imprime todas las citas al recibir un token de usuario admin    #COMPLETADO
@appcita.route('/citas') #get
def getAllDates():
    token = request.args.get('token')
    print(token)
    usuario = obtenerInfo(token)
    print(usuario)
    info_user = usuario['data']
    if info_user['admin']:
        output = []
        citas = Cita.query.all()
        for cita in citas:
            citaData = {}
            citaData['id'] = cita.id
            citaData['nombre'] = cita.mascota_id
            citaData['id_duenio'] = cita.user_id
            citaData['fecha'] = cita.fecha
            citaData['status'] = cita.status
            output.append(citaData)
    else:
        output.append('El usuario no es administrador')
    print("imprimiendo info del usuario desde /usuarios")
    #return jsonify({'citas':output})
    return render_template('printAllDates.html', citas = output, token = token)

#Imprime las citas por usuario       #COMPLETADO
@appcita.route('/citas-user') #get
def getMascotasUser():
    token = request.args.get('token')
    usuario = obtenerInfo(token)
    info_user = usuario['data']
    print(info_user)
    print(type(info_user))
    citas = Cita.query.filter_by(user_id=info_user['user_id'])
    print(citas)
    output = []
    if citas is not None:
        for cita in citas:
            citaData = {}
            citaData['id'] = cita.id
            citaData['mascota_id'] = cita.mascota_id
            citaData['id_duenio'] = cita.user_id
            citaData['fecha'] = cita.fecha
            citaData['status'] = cita.status
            output.append(citaData)
    else:
        output.append('El usuario no tiene citas para ninguna de sus mascotas')
    return jsonify({'citas':output})