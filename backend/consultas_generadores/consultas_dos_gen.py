from typing import Generator, Tuple
from collections import defaultdict

from utilidades import (
    Nave,
    Planeta,
    PlanetaMineral,
    Mision
)


# Consultas 2 generadores

def disponibilidad_por_planeta_import(generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                               generador_planetas: 
                               Generator[Planeta, None, None], id_mineral: int) -> Generator[Tuple[str, int, float], None, None]:
    
    cantidad_por_planeta = defaultdict(float)

    for planeta_mineral in generador_planeta_mineral:
        
        if planeta_mineral.id_mineral == id_mineral:
            cantidad_por_planeta[planeta_mineral.id_planeta] = planeta_mineral.cantidad_disponible

    for planeta in generador_planetas:
        cantidad_de_mineral_disponible = cantidad_por_planeta.get(planeta.id_planeta, 0.0)

        yield(planeta.nombre, planeta.id_planeta, cantidad_de_mineral_disponible)


def misiones_por_tipo_planeta_import(generador_misiones: Generator[Mision, None, None],
                              generador_planetas: 
                              Generator[Planeta, None, None], tipo: str) -> Generator[Mision, None, None]:
    
    mision_realizada = filter(lambda mision: mision.lograda != 
                              None, generador_misiones)
    
    planeta_por_tipo = defaultdict(str)

    for planeta in generador_planetas:
        
        if planeta.tipo == tipo:
            planeta_por_tipo[planeta.id_planeta] = planeta.tipo

    return filter(lambda mision: mision.id_planeta in planeta_por_tipo, mision_realizada)


def naves_pueden_llevar_import(generador_naves: Generator[Nave, None, None], generador_planeta_mineral: 
                               Generator[PlanetaMineral, None, None], 
                        id_planeta: int) -> Generator[tuple[str, int, float], None, None]:
    
    cantidad_por_mineral = defaultdict(float)
    for planeta_mineral in generador_planeta_mineral:
        
        if planeta_mineral.id_planeta == id_planeta:
            cantidad_por_mineral[planeta_mineral.id_mineral] = planeta_mineral.cantidad_disponible

    for nave in generador_naves:
        
        for id_mineral, cantidad_disponible in cantidad_por_mineral.items():
            valor_real = min(nave.capacidad_minerales, cantidad_disponible)
            porcentaje = (valor_real / cantidad_disponible) * 100

            yield (nave.patente, id_mineral, porcentaje)