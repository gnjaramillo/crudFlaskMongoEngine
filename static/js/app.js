// app.js

fetch('/obtenerCategorias')
.then(response => response.json())
.then(data => {
  const categorias = JSON.parse(data.categorias);
  // Ahora categorias es una lista de objetos JSON que puedes iterar
  categorias.forEach(categoria => {
    // Hacer algo con cada categoría, por ejemplo:
    console.log(categoria.nombre);
  });
});




fetch('/obtenerProductos')
.then(response => response.json())
.then(data => {
  const productos = JSON.parse(data.productos);
  // Ahora productos es una lista de objetos JSON que puedes iterar
  productos.forEach(producto => {
    // Hacer algo con cada producto, por ejemplo:
    console.log(producto.nombre);
  });
});




let base64URL = null; // Inicializar la variable base64URL

async function visualizarFoto(evento){
    const files = evento.target.files;
    const archivo = files[0];
    let filename = archivo.name;
    let extension = filename.split('.').pop().toLowerCase(); // Obtener la extensión del archivo
    if(extension !== 'jpg'){
        fileFoto.value = "";
        swal.fire("Seleccionar", "La imagen debe ser en formato JPG", "warning");
    } else {
        base64URL = await encodeFileAsBase64URL(archivo);
        const objectURL = URL.createObjectURL(archivo);
        imagenProducto.setAttribute("src", objectURL);
    }
}




/**
 * Returns a file in Base64URL format.
 * @param {File} file
 * @return {Promise<string>}
 */
async function encodeFileAsBase64URL(file) {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.addEventListener('loadend', () => {
            resolve(reader.result);
        });
        reader.readAsDataURL(file);
    });
}




function agregarProducto() {
    // Obtener los datos del formulario
    const codigo = document.getElementById('codigo').value;
    const nombre = document.getElementById('nombre').value;
    const precio = document.getElementById('precio').value;
    const categoria = document.getElementById('cdCategoria').value;
    const foto = base64URL; // Usar la variable base64URL

    // Crear un objeto FormData con los datos del formulario
    const formData = new FormData();
    formData.append('codigo', codigo);
    formData.append('nombre', nombre);
    formData.append('precio', precio);
    formData.append('categoria', categoria);
    formData.append('foto', foto);

    // Enviar los datos al servidor
    fetch('/agregarProducto', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Manejar la respuesta del servidor, por ejemplo, mostrar un mensaje de éxito o actualizar la lista de productos
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}




function consultarProducto(codigo) {
    fetch(`/consultarProducto/${codigo}`)
    .then(response => response.json())
    .then(data => {
        // Verificar si se encontró el producto
        if (data.estado) {
            // Redirigir a la página de edición del producto con los detalles del producto cargados
            window.location.href = `/editarProducto/${codigo}`;
        } else {
            // Mostrar un mensaje de error si el producto no se encontró
            swal.fire("Error", "Producto no encontrado", "error");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}




function editarProducto() {
    // Obtener los datos del formulario
    const producto={
        codigo: codigo.value,
        nombre: nombre.value,
        precio: precio.value,
        categoria: cbCategoria.value
    
    }

    const foto = {
        foto: base64url 
    } // Esta es la imagen en formato base64 obtenida del archivo seleccionado PROFRESOR

    const datos = {

        producto:producto,
        foto:foto
    }

    fetch('/editarProducto', {
        method: 'POST',
        body: JSON.stringify(datos),
        headers:{
            "Content-Type": "application/json",
        },
    })
    .then(response => response.json())
    .then(resultado  =>{
        console.log(resultado)    
        if (resultado.estado) {
            formEditProducto.reset()
            swal.fire("Editar Producto", resultado.mensaje, "success")



        } else {
            swal.fire("Editar Producto", resultado.mensaje, "warning")
        }
    });

} 




    
//eliminar producto    
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.btneliminar').forEach(btn => {
            btn.addEventListener('click', function(event) {
                event.preventDefault();
                
                const productoId = this.getAttribute('data-producto-id');
                
                // Mostrar el cuadro de diálogo de confirmación
                Swal.fire({
                    title: '¿Estás seguro de eliminar este producto?',
                    text: 'Esta acción no se puede deshacer.',
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Sí, eliminarlo'
                }).then((result) => {
                    if (result.isConfirmed) {
                        // El usuario confirmó la eliminación, proceder con la solicitud DELETE
                        eliminarProducto(productoId);
                    }
                });
            });
        });
        
        function eliminarProducto(_id) {
            $.ajax({
                url: '/eliminarProducto/' + _id,
                type: 'DELETE',
                success: function(response) {
                    Swal.fire({
                        icon: 'success',
                        title: response.message,
                        showConfirmButton: false,
                        timer: 3000
                    });
                    
                    // Eliminar el elemento de la lista de productos en la interfaz de usuario
                    $("#producto_" + _id).remove(); // Suponiendo que el ID del elemento de la lista es "producto_<_id>"
                },
                error: function(xhr, status, error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Error al eliminar el producto: ' + xhr.responseText,
                    });
                }
            });
        }
    });
    