from flask import Flask, jsonify, request, Blueprint
from flask_mysqldb import MySQL
from flask_cors import CORS 
from blueprints.alumnos.routes import alumnos_bp
from blueprints.maestros.routes import maestros_bp

from config import config

app = Flask(__name__)
app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)

CORS(app)

con = MySQL(app)


def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>"


if __name__=="__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(host='0.0.0.0',port=5000)