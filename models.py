# modelos.py

from mongoengine import Document, StringField, ReferenceField, IntField

class Usuarios(Document):
    correo = StringField(required=True)
    contraseña = StringField(required=True)

class Categorias(Document):
    nombre = StringField(required=True, unique=True, max_length=50)

class Productos(Document):
    codigo = IntField(required=True)
    nombre = StringField(required=True)
    precio = IntField()
    categoria = ReferenceField(Categorias, required=True)
