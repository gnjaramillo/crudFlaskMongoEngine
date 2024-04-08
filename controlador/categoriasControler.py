#categoriasControler.py
""" from app import app
from flask import jsonify
from models import Categorias
from bson.json_util import dumps

@app.route('/obtenerCategorias')
def obtenerCategorias():
    try:
        cat = Categorias.objects()
        listaCategorias = list(cat)
        json_data = dumps(listaCategorias)
        retorno = {'categorias': json_data}
        return jsonify(retorno)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True) """



from app import app
from flask import jsonify
from models import Categorias

@app.route('/obtenerCategorias')
def obtenerCategorias():
    try:
        categorias = Categorias.objects()
        listaCategorias = [{'id': str(c.id), 'nombre': c.nombre} for c in categorias]
        retorno = {'categorias': listaCategorias}
        return jsonify(retorno)
    except Exception as e:
        return jsonify({'error': str(e)})
