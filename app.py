from flask import Flask,request,jsonify, render_template
from flask_cors import CORS
from database import db
from encriptador import bcrypt
from flask_migrate import Migrate
from config import BaseConfig

from routes.user.user import appuser
from routes.mascotas.mascota import appmascota
#from routes.images.images import imageUser
app = Flask(__name__)
app.register_blueprint(appuser)
app.register_blueprint(appmascota) #agregando appmascota
#app.register_blueprint(imageUser)
app.config.from_object(BaseConfig)

CORS(app)

bcrypt.init_app(app)
db.init_app(app)
#configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

# Mostrando el index
@app.route('/')
def index():
    return render_template('index.html')

#Agregando pagina de error 404
def pagina_no_encontrada(error):
    return render_template('404.html')

app.register_error_handler(404,pagina_no_encontrada)

#Agregando pagina de error 400
def peticion_mala(error):
    return render_template('400.html')

app.register_error_handler(400,peticion_mala)

#RUTAS PROTEGIDAS

#prueba
@app.route('/logeandose', methods =['POST'])
def logeandose():
    nombreUser = request.form['email'] #add 02-12-22
    print('RECIBO NOMBRE DE USUARIO:')
    print(nombreUser)
    userPass = request.form['password'] #add 02-12-22
    print('RECIBO LA PASS:')
    print(userPass)
    return "<h1>Bienvenido " + nombreUser + "</h1>"