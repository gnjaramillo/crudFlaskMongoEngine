# productosControler.py

import os
from PIL import Image
from io import BytesIO
import base64
from flask import render_template, request, jsonify, redirect, url_for, session
from app import app
from models import Productos, Categorias
from bson.json_util import dumps
from flask import render_template, request, redirect, url_for, session
from app import app
from models import Productos, Categorias  # Importa los modelos de MongoEngine

@app.route("/listaProductos", methods=['GET', 'POST'])
def listaProductos():
    mensaje_producto_agregado = request.args.get('mensaje_producto_agregado', None)  # Obtener el mensaje de producto agregado de la consulta
    mensaje_inicio_sesion = request.args.get('mensaje_inicio_sesion', None)  # Obtener el mensaje de inicio de sesión de la consulta
    estado = request.args.get('estado', False) 

    if 'usuario' in session:
        # Si el usuario ha iniciado sesión, se muestran los productos
        listaProductos = Productos.objects()
        listaCategorias = Categorias.objects()

        # Construir la lista de productos con las categorías incluidas
        listaP = []
        for p in listaProductos:
            categoria = Categorias.objects(id=p.categoria.id).first()
            if categoria:
                p.categoria = categoria.nombre
            else:
                p.categoria = "Sin categoría"
            listaP.append(p)

        # Si hay un mensaje de inicio de sesión en la sesión, se elimina
        if 'mensaje_inicio_sesion' in session:
            session.pop('mensaje_inicio_sesion')

        # Se renderiza la plantilla de lista de productos
        return render_template('listaProductos.html', productos=listaP, listaCategorias=listaCategorias, mensaje_producto_agregado=mensaje_producto_agregado, mensaje_inicio_sesion=mensaje_inicio_sesion, estado=estado)        
    else:
        # Si el usuario no ha iniciado sesión, se redirige al formulario de inicio de sesión
        return redirect(url_for('login'))




@app.route('/vistaAgregarProducto', methods=['GET'])
def vistaAgregarProducto():
    categoriasbd = Categorias.objects.all()  # Obtiene todas las categorías utilizando el modelo Categoria
    return render_template('formAgregarProd.html', Categorias=categoriasbd)





@app.route('/agregarProducto', methods=['POST'])
def agregarProducto():
    mensaje = None
    estado = False
    try:
        # Datos traídos del formulario
        codigo = int(request.form['codigo'])
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        idCategoria = request.form['cdCategoria']  # Aquí obtenemos el ID de la categoría desde el formulario
        foto = request.files['fileFoto'] 
        # Buscamos el objeto de Categoría correspondiente al ID proporcionado
        categoria = Categorias.objects(id=idCategoria).first()

        # Creamos una instancia del modelo Producto y asignamos la categoría correspondiente
        producto = Productos(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            categoria=categoria  # Asignamos el objeto de Categoría al campo categoria
        )
        
        # Guardamos el producto en la base de datos
        producto.save()
        if producto:
            idProducto = producto.id 
            nombreFotos = f'{idProducto}.jpg'
            #.save() metodo para guardar la imagen adjunta en el sistema de archivos del servidor
            #os.path.join(): Este es un método del módulo os en Python que se utiliza para unir componentes de ruta en una cadena de ruta. En este caso, se utiliza para concatenar la ruta del directorio de carga (UPLOAD_FOLDER) con el nombre del archivo (nombreFotos), 
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFotos))
            mensaje = 'Producto Agregado Correctamente'
            estado = True
        else:
            mensaje = 'Problema Al Agregar El Producto'
        estado = True
    except Exception as error:
        mensaje = str(error)
    
    return redirect(url_for('listaProductos', mensaje_producto_agregado=mensaje, estado=estado))





@app.route('/agregarProductoJson', methods=['POST'])
def agregarProductoJson():
    # Inicializar variables para el estado y el mensaje de la operación
    estado = False
    mensaje = None
    
    try:
        # Recibe los datos en formato JSON desde la solicitud
        datos = request.json
        
        # Extrae los datos del producto y la foto del JSON recibido
        producto = datos.get('producto')
        fotoBase64 = datos.get('foto')["foto"]
        
        # Busca la categoría por su ID
        categoria = Categorias.objects(id=producto["categoria"]).first()
        
        if not categoria:
            raise Exception('Categoría no encontrada')
        
        # Crea un nuevo producto utilizando el modelo de MongoEngine
        producto = Productos(
            codigo=int(producto["codigo"]),
            nombre=producto["nombre"],
            precio=int(producto["precio"]),
            categoria=categoria
        )
        producto.save()  # Guarda el producto en la base de datos
        
        if producto:
            idProducto = producto.id 
            rutaImagen = f"{os.path.join(app.config['UPLOAD_FOLDER'])}/{idProducto}.jpg"
            
            # Extrae la parte base64 de la imagen recibida y la decodifica
            fotoBase64 = fotoBase64[fotoBase64.index(',') + 1]
            fotoDecodificada = base64.b64decode(fotoBase64)
            
            # Abre la imagen decodificada y la guarda en formato JPEG en la ruta especificada
            imagen = Image.open(BytesIO(fotoDecodificada))
            imagenJpg = imagen.convert('RGB')
            imagen.save(rutaImagen)
            mensaje = 'Producto Agregado Correctamente'
            estado = True
        else:
            mensaje = 'Problema Al Agregar El Producto'






        
        # Define la ruta donde se guardará la imagen del producto
        rutaImagen = f"{app.config['UPLOAD_FOLDER']}/{producto.id}.jpg"
        
        # Extrae la parte base64 de la imagen recibida y la decodifica
        fotoBase64 = fotoBase64[fotoBase64.index(',') + 1]
        fotoDecodificada = base64.b64decode(fotoBase64)
        
        # Abre la imagen decodificada y la guarda en formato JPEG en la ruta especificada
        with open(rutaImagen, "wb") as f:
            f.write(fotoDecodificada)
        
        # Actualiza el estado y el mensaje de la operación
        estado = True
        mensaje = 'Producto Agregado correctamente'
        
    except Exception as error:
        # Captura cualquier excepción y actualiza el mensaje
        mensaje = str(error)
    
    # Retorna la respuesta en formato JSON con el estado y el mensaje de la operación
    retorno = {"estado": estado, "mensaje": mensaje}
    return jsonify(retorno)




from flask import jsonify
from models import Productos, Categorias
from bson.json_util import dumps

@app.route('/obtenerProductos')
def obtenerProductos():
    try:
        prods = Productos.objects()  # Obtiene todos los productos utilizando el modelo Producto
        listaProductos = []
        for prod in prods:
            # Obtener los datos de la categoría correspondiente al ID del producto
            categoria = prod.categoria
            if categoria:
                categoria_dict = categoria.to_mongo().to_dict()
                categoria_dict['_id'] = str(categoria_dict['_id'])  # Convertir ObjectId a cadena
                producto_dict = prod.to_mongo().to_dict()
                producto_dict['_id'] = str(producto_dict['_id'])  # Convertir ObjectId a cadena
                producto_dict['categoria'] = categoria_dict
                listaProductos.append(producto_dict)
        retorno = {'productos': listaProductos}
        return jsonify(retorno)
    except Exception as e:
        return jsonify({'error': str(e)})


    


    




@app.route('/consultarProducto/<codigo>', methods=['GET'])
def consultarProducto(codigo):
    estado = False
    mensaje = None
    producto = None
    listaCategorias = None
    try:
        # Intentamos obtener el producto por su código utilizando el modelo Producto
        producto = Productos.objects(codigo=codigo).first()
        if producto:
            estado = True
        listaCategorias = Categorias.objects()  # Obtenemos todas las categorías utilizando el modelo Categoria
    except Exception as error:
        mensaje = str(error)

    # Renderizamos la plantilla de edición de producto con la información obtenida
    return render_template('formEditarProd.html', producto=producto, categorias=listaCategorias)




@app.route("/editarProducto", methods=["POST"])
def editarProducto():
    estado = False
    mensajeEditProd = None
    try:
        codigo = int(request.form['codigo'])
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        idCategoria = request.form['cbCategoria']
        idProducto = request.form['idProducto']

        # Buscamos el producto a editar por su ID utilizando el modelo Producto
        producto = Productos.objects(id=idProducto).first()

        if producto:
            # Actualizamos los atributos del producto con los nuevos valores
            producto.codigo = codigo
            producto.nombre = nombre
            producto.precio = precio
            producto.categoria = idCategoria

            # Guardamos los cambios en la base de datos
            producto.save()

            mensajeEditProd = "Producto actualizado correctamente"
            estado = True
        else:
            mensajeEditProd = "El producto no se encontró en la base de datos"
    except Exception as error:
        mensajeEditProd = str(error)

    return render_template("formEditarProd.html", producto=producto, mensajeEditProd=mensajeEditProd, estado=estado)




@app.route('/eliminarProducto/<_id>', methods=['DELETE'])
def eliminarProducto(_id):
    try:
        # eliminar el producto por su ID utilizando el modelo Producto
        producto = Productos.objects(id=_id).first()
        if producto:
            producto.delete()  # eliminar el producto de la base de datos

            return jsonify({'message': 'Producto eliminado correctamente'}), 200
        else:
            return jsonify({'message': 'El producto no existe'}), 404
    except Exception as error:
        return jsonify({'message': 'Error al eliminar el producto', 'error': str(error)}), 500
