from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from sqlalchemy import exc
from models import Mascota
from app import db,bcrypt
from auth import tokenCheck, obtenerInfo
from models import User
from models import Cita
from flask_login import login_required
from json2excel import Json2Excel

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
    nombreMascota = request.form['nombre']
    #fechaCita = request.form['fecha']

    #ACTUALIZACION: Se recibe fecha y hora por separado para facil validacion
    fecha = request.form['date']
    hora = request.form['time']
    listaHorarios = ['19:00','18:00','17:00','16:00','15:00','14:00','13:00','12:00','11:00','10:00','09:00']
    if hora not in listaHorarios:
        mensaje = "Datos invalidos"
        return render_template('agregarCitas.html', token = token, mensaje = mensaje)
    
    fechaCita = fecha +' ' + hora
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
    return render_template('agregarCitas.html', token = token, mensaje = mensaje) 

#Imprime todas las citas al recibir un token de usuario admin    #COMPLETADO
@appcita.route('/citas') #get
def getAllDates():
    token = request.args.get('token')
    usuario = obtenerInfo(token)
    info_user = usuario['data']
    if info_user['admin']:
        output = []
        citas = Cita.query.all()
        for cita in citas:
            citaData = {}
            citaData['id'] = cita.id
            citaData['fecha'] = cita.fecha
            citaData['status'] = cita.status
            citaData['duenio'] = info_user['email']

            #obteniendo nombres de mascota
            #citaData['nombre_mascota'] = cita.mascota_id
            mascotaName = db.engine.execute('select nombre from public."Mascotas" where id = ' + str(cita.mascota_id) + ';').first()
            citaData['nombre_mascota'] = mascotaName[0]
            output.append(citaData)
    else:
        output.append('El usuario no es administrador')
    return render_template('printAllDates.html', citas = output, token = token)

#Genera excel de todas las citas al recibir un token de usuario admin    #COMPLETADO
@appcita.route('/citas-excel') #get
def GenerarExcel():
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
            citaData['id_duenio'] = cita.user_id
            citaData['fecha'] = cita.fecha
            citaData['status'] = cita.status
            citaData['duenio'] = info_user['email']
            #obteniendo nombres de mascota
            mascotaName = db.engine.execute('select nombre from public."Mascotas" where id = ' + str(cita.mascota_id) + ';').first()
            citaData['nombre_mascota'] = mascotaName[0]
            output.append(citaData)
        
        json2excel = Json2Excel(head_name_cols=["id","nombre_mascota","duenio","id_duenio","fecha","status"])
        ruta = json2excel.run(output)
    else:
        output.append('El usuario no es administrador')
    return render_template('GeneracionExcel.html', ruta = ruta, token = token)

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
            citaData['id_duenio'] = cita.user_id
            citaData['fecha'] = cita.fecha
            citaData['status'] = cita.status

            #obteniendo nombres de mascota
            mascotaName = db.engine.execute('select nombre from public."Mascotas" where id = ' + str(cita.mascota_id) + ';').first()
            citaData['nombre_mascota'] = mascotaName[0]
            output.append(citaData)
    else:
        output.append('El usuario no tiene citas para ninguna de sus mascotas')
    return render_template('printUserDates.html', citas = output, token = token)