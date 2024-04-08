from app import app
from flask import render_template, request, redirect, url_for, session
from models import Usuarios
import yagmail
import threading

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje_error = ""
    mensaje_inicio_sesion = ""

    def enviarCorreo(email, destinatarios, asunto, mensaje):
        email.send(to=destinatarios, subject=asunto, contents=mensaje)

    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        usuario = Usuarios.objects(correo=correo, contraseña=contrasena).first()

        if usuario:
            email = yagmail.SMTP('gnjaramillo16@gmail.com', 'wkje zjqc zujh ffka', encoding='UTF-8')
            asunto = "El usuario ha ingresado al sistema"
            mensaje = f"Se informa que el usuario {usuario.correo} ha ingresado al sistema"
            thread = threading.Thread(
                target=enviarCorreo,
                args=(email, ['gnjaramillo16@gmail.com', usuario.correo], asunto, mensaje)
            )
            thread.start()
            session['usuario'] = correo  
            mensaje_inicio_sesion = "Ha iniciado sesión correctamente."
            if 'mensaje_inicio_sesion' in session:
                mensaje_inicio_sesion = session.pop('mensaje_inicio_sesion')
            return redirect(url_for('listaProductos', mensaje_inicio_sesion=mensaje_inicio_sesion)) 
        else:
            mensaje_error = "Correo o contraseña incorrecto"

    return render_template('login.html', mensaje_error=mensaje_error)

@app.route('/salir')
def salir():
    session.clear()
    mensaje = "Ha cerrado sesión correctamente"
    return render_template("login.html", mensaje=mensaje)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
