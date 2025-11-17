from typing import Generator, Tuple
from math import pi
from collections import defaultdict


from utilidades import (
    Tripulacion,
    Planeta,
    Mineral,
    PlanetaMineral,
    Mision,
    MisionMineral,
    radio_planeta
)


# Consultas 3 generadores

def planetas_por_estadisticas_import(generador_mineral: Generator[Mineral, None, None], 
                                     generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                              generador_planeta: Generator[Planeta, None, None], 
                              moles_elemento_min: float, 
                              concentracion_molar_min: float, densidad_min: float) -> Generator[Planeta, None, None]:
    
    mineral_por_planeta = defaultdict(list)
    cantidad_mineral_por_planeta = defaultdict(float)
    pureza_mineral_por_planeta = defaultdict(float)
    masa_at_por_mineral = defaultdict(float)
    
    for planeta_mineral in generador_planeta_mineral:
        mineral_por_planeta[planeta_mineral.id_planeta].append(planeta_mineral.id_mineral)
        cantidad_mineral_por_planeta[(planeta_mineral.id_planeta, 
                                      planeta_mineral.id_mineral)] = planeta_mineral.cantidad_disponible
        
        pureza_mineral_por_planeta[(planeta_mineral.id_planeta, 
                                    planeta_mineral.id_mineral)] = planeta_mineral.pureza

    for mineral in generador_mineral:
        masa_at_por_mineral[mineral.id_mineral] = mineral.masa_atomica
        
    for planeta in generador_planeta:
        minerales_por_planeta = mineral_por_planeta[planeta.id_planeta]

        for mp in minerales_por_planeta:
            cantidad_disponible = cantidad_mineral_por_planeta[(planeta.id_planeta, mp)]
            pureza_mineral = pureza_mineral_por_planeta[(planeta.id_planeta, mp)]
            masa_at = masa_at_por_mineral[mp]

            volumen = (4/3) * pi * (radio_planeta(planeta.id_planeta, planeta.tamano)**3)

            # Calculos 
            moles_elemento = ((cantidad_disponible * 1000000)) * pureza_mineral / masa_at
            concentracion_molar = ((cantidad_disponible * 1000000) * pureza_mineral) / (volumen * masa_at)
            densidad = ((cantidad_disponible * 1000000) * pureza_mineral) / volumen

            if (moles_elemento >= moles_elemento_min and
                concentracion_molar >= concentracion_molar_min and
                densidad >= densidad_min):

                yield planeta
                break


def ganancias_potenciales_por_planeta_import(generador_minerales: Generator[Mineral, None, None], 
                                             generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                                      generador_planetas: Generator[Planeta, None, None], precios: dict) -> dict:
    
    mineral_por_planeta = defaultdict(list)
    cantidad_mineral_por_planeta = defaultdict(float)
    pureza_mineral_por_planeta = defaultdict(float)
    id_mineral_por_nombre = defaultdict(str)
    
    for planeta_mineral in generador_planeta_mineral:
        mineral_por_planeta[planeta_mineral.id_planeta].append(planeta_mineral.id_mineral)
        cantidad_mineral_por_planeta[(planeta_mineral.id_planeta, 
                                      planeta_mineral.id_mineral)] = planeta_mineral.cantidad_disponible
        
        pureza_mineral_por_planeta[(planeta_mineral.id_planeta, 
                                    planeta_mineral.id_mineral)] = planeta_mineral.pureza

    for mineral in generador_minerales:
        id_mineral_por_nombre[mineral.id_mineral] = mineral.nombre

    planetas_devolver = defaultdict(float)

    for planeta in generador_planetas:
        id_planeta = planeta.id_planeta
        valor_total = 0

        minerales_por_planeta = mineral_por_planeta[planeta.id_planeta]

        for mp in minerales_por_planeta:
            if id_mineral_por_nombre[mp] in precios:
                precio_mineral = precios[id_mineral_por_nombre[mp]]
                cantidad_pura = (cantidad_mineral_por_planeta[(planeta.id_planeta, mp)] * 
                                pureza_mineral_por_planeta[(planeta.id_planeta, mp)])
                
                valor_total += precio_mineral * cantidad_pura

        planetas_devolver[id_planeta] = valor_total

    return planetas_devolver


def planetas_visitados_por_nave_import(generador_planetas: Generator[Planeta, None, None], 
                                       generador_misiones: Generator[Mision, None, None], 
                                generador_tripulaciones: Generator[Tripulacion, None, None]) -> Generator[Tuple[str, 
                                str|None, int|None], None, None]:
    
    nombre_por_planeta = defaultdict(str)
    patente_por_equipo = defaultdict(str)
    
    for planeta in generador_planetas:
        nombre_por_planeta[planeta.id_planeta] = planeta.nombre

    for tripulante in generador_tripulaciones:
        patente_por_equipo[tripulante.id_equipo] = tripulante.patente_nave

    tuplas_validas = set()

    for mision in generador_misiones:
        
        if mision.lograda != None:
            patente = patente_por_equipo.get(mision.id_equipo)
            
            if patente:
                nombre_planeta = nombre_por_planeta.get(mision.id_planeta)
                tuplas_validas.add((patente, nombre_planeta, mision.id_planeta))


    patentes_con_visitas = set()
    for t in tuplas_validas:
        patentes_con_visitas.add(t[0])

    for patente in patente_por_equipo.values():
        if patente not in patentes_con_visitas:
            tuplas_validas.add((patente, None, None))

    for t in tuplas_validas:
        yield t


def mineral_por_nave_import(generador_tripulaciones: 
                            Generator[Tripulacion, None, None], 
                            generador_misiones: Generator[Mision, None, None], 
                     generador_misiones_mineral: 
                     Generator[MisionMineral, None, None]) -> Generator[Tuple[str, float], None, None]:
    
    patente_por_equipo = defaultdict(str)
    equipo_por_mision_lograda = defaultdict(int)
    mineral_por_patente = defaultdict(float)
    
    for tripulante in generador_tripulaciones:
        patente_por_equipo[tripulante.id_equipo] = tripulante.patente_nave

    for mision in generador_misiones:
        
        if mision.lograda is True:
            equipo_por_mision_lograda[mision.id_mision] = mision.id_equipo

    for mm in generador_misiones_mineral:
        
        if mm.id_mision in equipo_por_mision_lograda:
            id_equipo = equipo_por_mision_lograda[mm.id_mision]
            patente = patente_por_equipo.get(id_equipo)
            
            if patente:
                mineral_por_patente[patente] += mm.cantidad

    for patente in patente_por_equipo.values():
        total = mineral_por_patente.get(patente, 0.0)
        yield (patente, total)


def porcentaje_extraccion_import(generador_tripulacion: Generator[Tripulacion, None, None], 
                                 generador_mision_mineral: Generator[MisionMineral, None, None], 
                          generador_planeta_mineral: 
                          Generator[PlanetaMineral, None, None], mision : Mision) -> Tuple[float, float]:
    
    cantidad_por_mision_y_mineral = defaultdict(float)
    minerales_por_mision = defaultdict(list)
    puro_por_planeta_y_mineral = defaultdict(float)
    tripulantes_por_equipo = defaultdict(list)

    for mision_m in generador_mision_mineral:
        cantidad_por_mision_y_mineral[(mision_m.id_mision, 
                                       mision_m.id_mineral)] += mision_m.cantidad
        
        minerales_por_mision[mision_m.id_mision].append(mision_m.id_mineral)

    for planeta_m in generador_planeta_mineral:
        cantidad_pura = planeta_m.cantidad_disponible * planeta_m.pureza
        
        puro_por_planeta_y_mineral[(planeta_m.id_planeta, 
                                    planeta_m.id_mineral)] += cantidad_pura

    for t in generador_tripulacion:
        tripulantes_por_equipo[t.id_equipo].append(t.id_astronauta)

    if not mision.lograda:
        return (0.0, 0.0)

    planeta = mision.id_planeta
    porcentaje_extraido_del_planeta = 0.0

    total_puro_planeta = 0.0
    total_extraido = 0.0

    for id_mineral in minerales_por_mision.get(mision.id_mision, []):
        cantidad_extraida = cantidad_por_mision_y_mineral[(mision.id_mision, id_mineral)]
        cantidad_total_pura = puro_por_planeta_y_mineral.get((planeta, id_mineral), 0.0)
        total_puro_planeta += cantidad_total_pura
        total_extraido += cantidad_extraida

    if total_puro_planeta > 0:
        porcentaje_extraido_del_planeta = (total_extraido * 100) / total_puro_planeta

    n_tripulantes = len(tripulantes_por_equipo.get(mision.id_equipo, []))
    
    if n_tripulantes > 0:
        porcentaje_por_tripulante = porcentaje_extraido_del_planeta / n_tripulantes
    
    else:
        porcentaje_por_tripulante = 0.0 

    return (porcentaje_extraido_del_planeta, porcentaje_por_tripulante)