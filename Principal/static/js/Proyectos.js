$("#id_photo").on("change", (e) => {
    const archivo = $(e.target)[0].files[0];
    let nombArchivo = archivo.name;
    var extension = nombArchivo.split(".").slice(-1);
        extension = extension[0];
    let extensiones = ["jpg", "png", "jpeg","webp"];
   
    if(extensiones.indexOf(extension) === -1){
      document.getElementById('id_photo').value = '';
    }else{
    }
    
  });