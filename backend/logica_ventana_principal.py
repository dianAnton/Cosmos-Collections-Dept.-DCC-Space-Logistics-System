from os import path
from PyQt5.QtWidgets import ( 
    QFileDialog, QMessageBox
)
from backend import consultas
from frontend.ventanas.ventana_mapa import VentanaMapa


# Seleccionar archivo a abrir
def abrir_archivo_import(self):
    print("Abriendo diálogo de archivo...")
    
    # QFileDialog.getOpenFileName retorna una tupla (path_archivo, filtro)
    ruta, _ = QFileDialog.getOpenFileName(
        self, 
        
        # Nombre de la ventana
        "Seleccionar archivo de datos", 

        # Directorio del cual se buscan los archivos
        "",

        # Filtrp
        "Archivos de Datos (*.csv *.json *.txt)"
    )
    
    if ruta:
        self.archivo_path = ruta
        
        # Mostramos solo el nombre del archivo, no la ruta completa
        nombre_archivo = path.basename(ruta)
        self.path_label.setText(f"Archivo: {nombre_archivo}")
        print(f"Archivo seleccionado: {ruta}")

    else:
        print("Selección de archivo cancelada.")


# Ejecutar una consulta, manejo
def ejecutar_consulta_import(self):
    print("Ejecutando consulta...")
    
    # Comprobar que el archivo esta cargado
    if not self.archivo_path:
        QMessageBox.warning(self, "Error: Archivo no cargado",
                            "Por favor, sube un archivo antes de ejecutar una consulta.")
        return

    # Obtener el texto (query) dada en el input
    query_texto = self.query_input.text().strip()

    if not query_texto:
        QMessageBox.warning(self, "Error: Consulta vacía",
                            "Por favor, ingresa una entidad (ej: 'Astronauta') para consultar.")
        return

    partes = query_texto.split(',', 1)
    partes_separadas = []
    
    for p in partes:
        partes_separadas.append(p.strip())

    entidad = partes_separadas[0]
    
    # comprobar que se haya pasado algun filtor
    if len(partes_separadas) > 1:
        filtro_text = partes_separadas[1]
    
    else:
        filtro_text = ""

    # Mapear nombres de entidad a funciones cargar
    cargar_entidades = {
        'astronauta': consultas.cargar_astronautas,
        'nave': consultas.cargar_naves,
        'tripulacion': consultas.cargar_tripulaciones,
        'planeta': consultas.cargar_planetas,
        'mineral': consultas.cargar_minerales,
        'planetamineral': consultas.cargar_planeta_minerales,
        'mision': consultas.cargar_mision,
        'misionmineral': consultas.cargar_materiales_mision,
    }

    # Quitar todo espacio
    clave = entidad.replace(" ", "").lower()
    
    if clave not in cargar_entidades:
        QMessageBox.critical(self, "Entidad desconocida",
                            f"La entidad '{entidad}' no es soportada por la aplicación.")
        return

    # Obtener la funcion para cargar la entidad dada
    cargar_func = cargar_entidades[clave]

    # Intentar cargar el archivo y guardar el generador de instancias de entidades
    try:
        gen = cargar_func(self.archivo_path)
    
    except (AttributeError, TypeError, ValueError) as error:
        QMessageBox.critical(self, "Error al cargar archivo",
                            f"No se pudo cargar la entidad desde el archivo: {error}")
        return

    # Parsear (analizar texto y convertilo a el formato adecuado) filtros
    filtros = {}
    
    if filtro_text:
        
        # Soporta multiples filtros separados por ','
        condiciones = []
        for c in filtro_text.split(','):
            c = c.strip()
            if '=' in c:
                condiciones.append(c)
        
        for condicion in condiciones:
            atributo, valor = condicion.split('=', 1)
            filtros[atributo.strip()] = valor.strip()

    # Filtrado de resultados
    # Aplicar filtros y construir salida
    resultados = []
    
    try:
        for instancia in gen:

            # Si no hay filtror, agrega la instancia completa
            if not filtros:
                resultados.append(instancia)
                continue

            condicional = True
            for atributo, valor in filtros.items():
                
                attr = None
                tipo_instancia = type(instancia)

                # Obtener los campos de las instancias de la namedtuple
                clase_dict = tipo_instancia.__dict__

                # Detectar manualmente si es namedtuple
                if "_fields" in clase_dict:
                    campos = clase_dict["_fields"]
                    if atributo in campos:
                        index = campos.index(atributo)
                        attr = instancia[index]
                    else:
                        condicional = False
                        break

                # Si es diccionario
                elif isinstance(instancia, dict):
                    if atributo in instancia:
                        attr = instancia[atributo]
                    else:
                        condicional = False
                        break

                # Tipo desconocido
                else:
                    condicional = False
                    break
                
                # si el atributo no coincide con el valor buscado, cambiamos el condicional
                if str(attr) != valor:
                    condicional = False
                    break
            
            # Si la condicion se cumple, guardamos la instancia filtrada en resiltados
            if condicional:
                resultados.append(instancia)

    except (AttributeError, TypeError, ValueError) as error:
        QMessageBox.critical(self, "Error al filtrar", f"Error procesando datos: {error}")
        return

    # Mostrar resultados en la area de texto
    self.results_area.clear()
    
    if not resultados:
        self.results_area.append("No se encontraron resultados.")
    
    else:
        for item in resultados:
            self.results_area.append(str(item))


# Abrir la ventana mapa
def abrir_mapa_import(self):
    print("Abriendo el mapa...")

    # Verificar si hay un archivo cargado
    if not self.archivo_path:
        QMessageBox.warning(self, "Archivo planetas faltante", 
                            "Por favor sube el archivo de planetas antes de abrir el mapa.")
        return

    # Verificar que el archivo cargado sea Planeta.csv
    nombre_archivo = path.basename(self.archivo_path)
    
    if nombre_archivo != 'Planeta.csv':
        QMessageBox.warning(self, "Archivo de Planetas Incorrecto", 
                            f"El mapa solo puede abrir el archivo 'Planeta.csv'")
        return

    # abrir la ventana mapa
    self.mapa_window = VentanaMapa(self.archivo_path)
    self.mapa_window.senal_cerrar.connect(lambda: self.show())
    self.hide()
    self.mapa_window.show()