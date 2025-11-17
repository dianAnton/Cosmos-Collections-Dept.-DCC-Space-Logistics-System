from typing import Generator, List, Tuple
from itertools import islice

from collections import defaultdict

from datetime import date

from utilidades import (
    Nave,
    Tripulacion,
    Planeta,
    PlanetaMineral,
    Mision,
)


# Consultas 1 generador

def naves_de_material_import(generador_naves: Generator[Nave, None, None], 
                             material: str) -> Generator[Nave, None, None]:  
    
    # Naves cuyo material coincide con el material de nave recibido
    return filter(lambda nave: material == nave.material, generador_naves)


def misiones_desde_fecha_import(generador_misiones: Generator[Mision, None, None], 
                                fecha: str, inverso: bool) -> Generator[Mision, None, None]:
    
    # Manejar la fecha como un objeto
    fecha_date = date.fromisoformat(fecha)

    if inverso == False:
        return filter(lambda mision: date.fromisoformat(mision.fecha) >= fecha_date, 
                      generador_misiones)
    
    elif inverso == True:
        return filter(lambda mision: date.fromisoformat(mision.fecha) <= fecha_date, 
                      generador_misiones)
    

def naves_por_intervalo_carga_import(generador_naves: Generator[Nave, None, None], 
                                     cargas: tuple[float, float]) -> Generator[Nave, None, None]:
    
    carga_minima = cargas[0]
    carga_maxima = cargas[1]
    
    return filter(lambda nave: carga_minima <= nave.capacidad_minerales <= carga_maxima,
                  generador_naves)


def planetas_con_cantidad_de_minerales_import(generador_planeta_mineral: Generator[PlanetaMineral, 
                                                                                   None, None], 
                                              id_mineral: int, cantidad_minima: int) -> List[int]:
    
    planetas_mineral = filter(lambda planeta: id_mineral == planeta.id_mineral, 
                              generador_planeta_mineral)

    planetas_compatibles = filter(lambda planeta: cantidad_minima <= 
                                  (planeta.cantidad_disponible * planeta.pureza), 
                                  planetas_mineral)
    
    planetas_cantidad_neta_minima = []
    
    for planeta in planetas_compatibles:
        planetas_cantidad_neta_minima.append(planeta.id_planeta)

    return planetas_cantidad_neta_minima


def naves_astronautas_rango_import(generador_tripulacion: Generator[Tripulacion, 
                                                                    None, None], rango: int, 
                            minimo_astronautas: int) -> Generator[Tuple[str, Generator], None, None]:
    
    # Filtar los astronautas con el rango correcto, por patente
    astronautas_por_nave = defaultdict(list)

    for tripulacion in generador_tripulacion:
        
        if tripulacion.rango >= rango:
            astronautas_por_nave[tripulacion.patente_nave].append(tripulacion.id_astronauta)

    for i in astronautas_por_nave:
        if minimo_astronautas < 1:
            yield(i, (item for item in astronautas_por_nave[i])) 

        elif len(astronautas_por_nave[i]) >= minimo_astronautas:
            yield(i, (item for item in astronautas_por_nave[i])) 

    
def cambiar_rango_astronauta_import(generador_tripulacion: Generator[Tripulacion, None, None], 
                                    id_astronauta: int, rango_astronauta: int) -> Generator[Tripulacion, None, None]:
    
    for astronauta in generador_tripulacion:
        
        if astronauta.id_astronauta == id_astronauta:
            astronauta_modificado = astronauta._replace(rango=rango_astronauta)
            yield astronauta_modificado
       
        else:
            yield astronauta


def encontrar_planetas_cercanos_import(generador_planetas: Generator[Planeta, 
                                                                     None, None], x1: int, 
                                y1: int, x2: int, y2: int, cantidad: int | None = None) -> Generator[Planeta, None, None]:

    planetas_filtrados = filter(lambda planeta: x1 <= 
                                planeta.coordenada_x <= x2 and 
                                y1 <= planeta.coordenada_y <= y2, generador_planetas)
    
    if cantidad is not None:
        planetas_filtrados = islice(planetas_filtrados, cantidad)
    
    return planetas_filtrados