from typing import Generator, List, Tuple
from collections import defaultdict

from .cargar_datos import (
    cargar_astronautas_import,
    cargar_naves_import,
    cargar_tripulaciones_import,
    cargar_planetas_import,
    cargar_minerales_import,
    cargar_planeta_minerales_import,
    cargar_mision_import,
    cargar_materiales_mision_import
)

from .consultas_generadores.consultas_un_gen import (
    naves_de_material_import,
    misiones_desde_fecha_import,
    naves_por_intervalo_carga_import,
    planetas_con_cantidad_de_minerales_import,
    naves_astronautas_rango_import,
    cambiar_rango_astronauta_import,
    encontrar_planetas_cercanos_import
)

from .consultas_generadores.consultas_dos_gen import (
    disponibilidad_por_planeta_import,
    misiones_por_tipo_planeta_import,
    naves_pueden_llevar_import
)

from .consultas_generadores.consultas_tres_gen import (
    planetas_por_estadisticas_import,
    ganancias_potenciales_por_planeta_import,
    planetas_visitados_por_nave_import,
    mineral_por_nave_import,
    porcentaje_extraccion_import
)

from utilidades import (
    Astronauta,
    Nave,
    Tripulacion,
    Planeta,
    Mineral,
    PlanetaMineral,
    Mision,
    MisionMineral,
    radio_planeta
)


# Cargas 

def cargar_astronautas(path: str) -> Generator[Astronauta, None, None]:
    return cargar_astronautas_import(path)


def cargar_naves(path: str) -> Generator[Nave, None, None]:
    return cargar_naves_import(path)

def cargar_tripulaciones(path: str) -> Generator[Tripulacion, None, None]:
    return cargar_tripulaciones_import(path)


def cargar_planetas(path: str) -> Generator[Planeta, None, None]:
    return cargar_planetas_import(path)


def cargar_minerales(path: str) -> Generator[Mineral, None, None]:
    return cargar_minerales_import(path)


def cargar_planeta_minerales(path: str) -> Generator[PlanetaMineral, None, None]:
    return cargar_planeta_minerales_import(path)


def cargar_mision(path: str) -> Generator[Mision, None, None]:
    return cargar_mision_import(path)


def cargar_materiales_mision(path: str) -> Generator[MisionMineral, None, None]:
    return cargar_materiales_mision_import(path)


# Consultas 1 generador

def naves_de_material(generador_naves: 
                      Generator[Nave, None, None], material: str) -> Generator[Nave, None, None]:  
    
    return naves_de_material_import(generador_naves, material)


def misiones_desde_fecha(generador_misiones: 
                         Generator[Mision, None, None], 
                         fecha: str, inverso: bool) -> Generator[Mision, None, None]:
    
    return misiones_desde_fecha_import(generador_misiones, fecha, inverso)
    

def naves_por_intervalo_carga(generador_naves: 
                              Generator[Nave, None, None], 
                              cargas: tuple[float, float]) -> Generator[Nave, None, None]:
    
    return naves_por_intervalo_carga_import(generador_naves, cargas)


def planetas_con_cantidad_de_minerales(generador_planeta_mineral: 
                                       Generator[PlanetaMineral, None, None], 
                                       id_mineral: int, cantidad_minima: int) -> List[int]:
    
    return planetas_con_cantidad_de_minerales_import(generador_planeta_mineral, 
                                                     id_mineral, cantidad_minima)


def naves_astronautas_rango(generador_tripulacion: 
                            Generator[Tripulacion, None, None], rango: int, 
                            minimo_astronautas: int) -> Generator[Tuple[str, Generator], None, None]:
    
    return naves_astronautas_rango_import(generador_tripulacion, 
                                          rango, minimo_astronautas)

    
def cambiar_rango_astronauta(generador_tripulacion: 
                             Generator[Tripulacion, None, None], 
                             id_astronauta: int, rango_astronauta: int) -> Generator[Tripulacion, None, None]:
    
    return cambiar_rango_astronauta_import(generador_tripulacion, 
                                           id_astronauta, rango_astronauta)


def encontrar_planetas_cercanos(generador_planetas: 
                                Generator[Planeta, None, None], x1: int, 
                                y1: int, x2: int, y2: int, cantidad: int | None = None) -> Generator[Planeta, None, None]:

    return encontrar_planetas_cercanos_import(generador_planetas, 
                                              x1, y1, x2, y2, cantidad)
   
 
# Consultas 2 generadores

def disponibilidad_por_planeta(generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                               generador_planetas: 
                               Generator[Planeta, None, None], 
                               id_mineral: int) -> Generator[Tuple[str, int, float], None, None]:
    
    return disponibilidad_por_planeta_import(generador_planeta_mineral, 
                                             generador_planetas, id_mineral)


def misiones_por_tipo_planeta(generador_misiones: Generator[Mision, None, None],
                              generador_planetas: 
                              Generator[Planeta, None, None], tipo: str) -> Generator[Mision, None, None]:
    
    return misiones_por_tipo_planeta_import(generador_misiones, 
                                            generador_planetas, tipo)


def naves_pueden_llevar(generador_naves: Generator[Nave, None, None], 
                        generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                        id_planeta: int) -> Generator[tuple[str, int, float], None, None]:
    
    return naves_pueden_llevar_import(generador_naves, 
                                      generador_planeta_mineral, id_planeta)


# Consultas 3 generadores

def planetas_por_estadisticas(generador_mineral: Generator[Mineral, None, None], generador_planeta_mineral: 
                              Generator[PlanetaMineral, None, None], 
                              generador_planeta: 
                              Generator[Planeta, None, None], moles_elemento_min: float, 
                              concentracion_molar_min: float, 
                              densidad_min: float) -> Generator[Planeta, None, None]:
    
    return planetas_por_estadisticas_import(generador_mineral, generador_planeta_mineral, 
                                                     generador_planeta, 
                                                     moles_elemento_min, concentracion_molar_min, 
                                                     densidad_min)

            
def ganancias_potenciales_por_planeta(generador_minerales: Generator[Mineral, None, None], 
                                      generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                                      generador_planetas: Generator[Planeta, None, None], precios: dict) -> dict:
    
    return ganancias_potenciales_por_planeta_import(generador_minerales, 
                                                    generador_planeta_mineral, 
                                                    generador_planetas, precios)


def planetas_visitados_por_nave(generador_planetas: Generator[Planeta, None, None], 
                                generador_misiones: Generator[Mision, None, None], 
                                generador_tripulaciones: 
                                Generator[Tripulacion, None, None]) -> Generator[Tuple[str, str|None, int|None], None, None]:
    
    return planetas_visitados_por_nave_import(generador_planetas, 
                                              generador_misiones, generador_tripulaciones)


def mineral_por_nave(generador_tripulaciones: Generator[Tripulacion, None, None], 
                     generador_misiones: Generator[Mision, None, None], 
                     generador_misiones_mineral: 
                     Generator[MisionMineral, None, None]) -> Generator[Tuple[str, float], None, None]:
    
    return mineral_por_nave_import(generador_tripulaciones, 
                                   generador_misiones, generador_misiones_mineral)


def porcentaje_extraccion(generador_tripulacion: 
                          Generator[Tripulacion, None, None], 
                          generador_mision_mineral: Generator[MisionMineral, None, None], 
                          generador_planeta_mineral: 
                          Generator[PlanetaMineral, None, None], mision : Mision) -> Tuple[float, float]:
    
    return porcentaje_extraccion_import(generador_tripulacion, 
                                        generador_mision_mineral, 
                                        generador_planeta_mineral, mision)


# Consultas 4 generadores

def resultado_mision(mision: Mision, generador_naves: Generator[Nave, None, None], 
                     generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                     generador_tripulaciones: Generator[Tripulacion, None, None], 
                     generador_mision_mineral: Generator[MisionMineral, None, None]) -> Mision:

    patente_nave = None
    for tp in generador_tripulaciones:
        
        if tp.id_equipo == mision.id_equipo:
            patente_nave = tp.patente_nave
            break

    if patente_nave is None:
        return Mision(mision.id_mision, mision.fecha, mision.hora,
                      mision.id_equipo, mision.id_planeta, False)

    capacidad_nave = None
    for nave in generador_naves:
        
        if nave.patente == patente_nave:
            capacidad_nave = nave.capacidad_minerales
            break

    if capacidad_nave is None:
        
        return Mision(mision.id_mision, mision.fecha, mision.hora,
                      mision.id_equipo, mision.id_planeta, False)

    minerales_requeridos = []
    for mm in generador_mision_mineral:
        
        if mm.id_mision == mision.id_mision:
            minerales_requeridos.append(mm)

    if not minerales_requeridos:
        
        return Mision(mision.id_mision, mision.fecha, mision.hora,
                      mision.id_equipo, mision.id_planeta, False)

    # defaultdict con un valor por defecto, con lambda
    minerales_planeta = defaultdict(lambda: (0.0, 0.0)) 
    for pm in generador_planeta_mineral:
        
        if pm.id_planeta == mision.id_planeta:
            minerales_planeta[pm.id_mineral] = (pm.cantidad_disponible, pm.pureza)

    total_requerido = 0.0
    todos_disponibles = True
    gatochico_requerido = None 

    for mm in minerales_requeridos:
        total_requerido += mm.cantidad
        
        if mm.id_mineral == 1:
            gatochico_requerido = mm.cantidad

        cantidad_disponible, _ = minerales_planeta.get(mm.id_mineral, (0.0, 0.0))
        
        if mm.cantidad > cantidad_disponible:
            todos_disponibles = False

    # Condicion 1
    if todos_disponibles and total_requerido < capacidad_nave:
        
        return Mision(mision.id_mision, mision.fecha, mision.hora,
                    mision.id_equipo, mision.id_planeta, True)

    # Condicion 2
    if gatochico_requerido is not None and gatochico_requerido < capacidad_nave:
        
        return Mision(mision.id_mision, mision.fecha, mision.hora,
                    mision.id_equipo, mision.id_planeta, True)

    # Si no se cumple ninguna condicion
    return Mision(mision.id_mision, mision.fecha, mision.hora,
                  mision.id_equipo, mision.id_planeta, False)
    