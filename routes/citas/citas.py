from flask import Blueprint, request,jsonify
from sqlalchemy import exc
from models import Mascota
from app import db,bcrypt
from auth import tokenCheck
from models import User
from flask_login import login_required

appmascitas = Blueprint('appmascitas',__name__,template_folder="templates")