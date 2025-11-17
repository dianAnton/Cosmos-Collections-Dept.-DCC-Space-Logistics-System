from typing import Generator

from utilidades import (
    Astronauta,
    Nave,
    Tripulacion,
    Planeta,
    Mineral,
    PlanetaMineral,
    Mision,
    MisionMineral,
)


# Cargas 

def cargar_astronautas_import(path: str) -> Generator[Astronauta, None, None]:
    with open(path, encoding="utf-8") as file:
        
        # Saltar la primera linea del .csv (header)
        next(file)
        for astronauta in file:
            id_astronauta, nombre, estado = astronauta.split(",")
            
            yield Astronauta(int(id_astronauta), str(nombre).strip(), str(estado).replace("\n", ""))


def cargar_naves_import(path: str) -> Generator[Nave, None, None]:
    with open(path, encoding="utf-8") as file:
        
        # Saltar la primera linea del .csv (header)
        next(file)
        for nave in file:
            (patente, material, tamano, capacidad_astronautas, 
             capcidad_minerales, autonomia) = nave.split(",")
            
            yield Nave(str(patente), str(material), str(tamano), 
                             int(capacidad_astronautas), float(capcidad_minerales),
                             float(autonomia))


def cargar_tripulaciones_import(path: str) -> Generator[Tripulacion, None, None]:
    with open(path, encoding="utf-8") as file:
        
        # Saltar la primera linea del .csv (header)
        next(file)
        for tripulacion in file:
            (id_equipo, patente_nave, id_astronauta, rango) = tripulacion.split(",")

            yield Tripulacion(int(id_equipo), str(patente_nave), int(id_astronauta), 
                             int(rango))


def cargar_planetas_import(path: str) -> Generator[Planeta, None, None]:
    with open(path, encoding="utf-8") as file:
        
        # Saltar la primera linea del .csv (header)
        next(file)
        for planeta in file:
            (id_planeta, nombre, coordenada_x, coordenada_y,
             tamano, tipo) = planeta.split(",")

            yield Planeta(int(id_planeta), str(nombre), float(coordenada_x), 
                          float(coordenada_y), str(tamano), str(tipo).replace("\n", ""))


def cargar_minerales_import(path: str) -> Generator[Mineral, None, None]:
    with open(path, encoding="utf-8") as file:
        
        # Saltar la primera linea del .csv (header)
        next(file)
        for mineral in file:
            (id_mineral, nombre, simbolo_quimico, 
             numero_atomico, masa_atomica) = mineral.split(",")

            yield Mineral(int(id_mineral), str(nombre), str(simbolo_quimico), 
                          int(numero_atomico), float(masa_atomica))


def cargar_planeta_minerales_import(path: str) -> Generator[PlanetaMineral, None, None]:
    with open(path, encoding="utf-8") as file:
        
        # Saltar la primera linea del .csv (header)
        next(file)
        for planeta_mineral in file:
            (id_planeta, id_mineral, 
             cantidad_disponible, pureza) = planeta_mineral.split(",")

            yield PlanetaMineral(int(id_planeta), int(id_mineral), 
                                 float(cantidad_disponible), 
                                 float(pureza))


def cargar_mision_import(path: str) -> Generator[Mision, None, None]:
    with open(path, encoding="utf-8") as file:
        
        # Saltar la primera linea del .csv (header)
        next(file)
        for mision in file:
            (id_mision, fecha, hora, 
             id_equipo, id_planeta, lograda) = mision.split(",")

            if lograda.strip() == "True":
                lograda = True

            elif lograda.strip() == "None":
                lograda = None

            elif lograda.strip() == "False":
                lograda = False

            yield Mision(int(id_mision), fecha, hora, int(id_equipo), 
                         int(id_planeta), lograda)


def cargar_materiales_mision_import(path: str) -> Generator[MisionMineral, None, None]:
    with open(path, encoding="utf-8") as file:
        
        # Saltar la primera linea del .csv (header)
        next(file)
        for mision_mineral in file:
            (id_mision, id_mineral, cantidad) = mision_mineral.split(",")

            yield MisionMineral(int(id_mision), int(id_mineral), float(cantidad))