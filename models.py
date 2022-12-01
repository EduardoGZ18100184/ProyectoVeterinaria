from app import db, bcrypt
import jwt
import datetime
from config import BaseConfig

#Clase Usuario
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    mascotas = db.relationship('Mascota', backref='user')
    citas = db.relationship('Cita', backref='user')         #Add 24-11-22

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password,BaseConfig.BCRYPT_LOG_ROUNDS
        ).decode()
        
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                BaseConfig.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, BaseConfig.SECRET_KEY,algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError as e:
            print(e)
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError as e:
            print(e)
            return 'Invalid token. Please log in again.'

#Clase Mascota
class Mascota(db.Model):
    __tablename__ = 'Mascotas' 

    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    raza = db.Column(db.String(250))
    tipo = db.Column(db.String(250))
    citas = db.relationship('Cita', backref='mascota') #Add 24-11-22

    def __str__(self) -> str:
        return (f'ID : {self.id} ,'
                f'Nombre : {self.nombre} ,'
                f'Dueño : {self.user_id} ,' #Add 23-11-22
                f'Raza: {self.apellido} ,'
                f'Tipo: {self.email}'
        )

#Clase Cita
class Cita(db.Model):
    __tablename__ = 'cita' 

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mascota_id = db.Column(db.Integer, db.ForeignKey('Mascotas.id'))
    fecha = db.Column(db.DateTime)
    status = db.Column(db.String(250))

    def __str__(self) -> str:
        return (f'ID : {self.id} ,'
                f'Dueño : {self.user_id} ,'
                f'Mascota : {self.mascota_id} ,'
                f'Fecha: {self.fecha} ,'
                f'Status: {self.status}'
        )