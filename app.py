# app.py

from flask import Flask
from mongoengine import connect



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/img'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Conexión a la base de datos utilizando MongoEngine
connect(db='CrudFlask', host='mongodb://localhost:27017/CrudFlask', port=27017)


from controlador.productosControler import *
from controlador.categoriasControler import *
from controlador.loginControler import *


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
