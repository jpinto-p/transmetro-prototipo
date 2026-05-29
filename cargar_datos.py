from app import app, db
from models import Municipalidad, Linea, Estacion, Bus, Piloto, Parqueo, Acceso, Guardia, Distancia
from werkzeug.security import generate_password_hash

def cargar_datos():
    with app.app_context():
        # 1. Municipalidades
        muni1 = Municipalidad(nombre="Municipalidad de Guatemala", direccion="Palacio Municipal")
        muni2 = Municipalidad(nombre="Municipalidad de Mixco", direccion="Mixco Centro")
        muni3 = Municipalidad(nombre="Municipalidad de Villa Nueva", direccion="Villa Nueva")
        db.session.add_all([muni1, muni2, muni3])
        db.session.commit()

        # 2. Pilotos
        pilotos = [
            Piloto(nombre="Juan Pérez", direccion="Zona 1", telefono="1234-5678", historial_educativo="Licencia tipo B"),
            Piloto(nombre="María López", direccion="Zona 5", telefono="8765-4321", historial_educativo="Licencia tipo B"),
            Piloto(nombre="Carlos Ramírez", direccion="Villa Nueva", telefono="4455-6677", historial_educativo="Curso defensivo"),
            Piloto(nombre="Ana Morales", direccion="Mixco", telefono="9988-7766", historial_educativo="8 años experiencia"),
        ]
        db.session.add_all(pilotos)
        db.session.commit()

        # 3. Líneas
        linea1 = Linea(nombre="Línea 1", distancia_total=12.5, municipalidad_id=muni1.id)
        linea6 = Linea(nombre="Línea 6", distancia_total=18.2, municipalidad_id=muni1.id)
        linea12 = Linea(nombre="Línea 12", distancia_total=9.8, municipalidad_id=muni1.id)
        linea_mixco = Linea(nombre="Mixco-Centro", distancia_total=15.0, municipalidad_id=muni2.id)
        db.session.add_all([linea1, linea6, linea12, linea_mixco])
        db.session.commit()

        # 4. Estaciones (con orden)
        estaciones_linea1 = [
            Estacion(nombre="Estación Central", capacidad_maxima=200, orden=1, linea_id=linea1.id, municipalidad_id=muni1.id),
            Estacion(nombre="Plaza Barrios", capacidad_maxima=150, orden=2, linea_id=linea1.id, municipalidad_id=muni1.id),
            Estacion(nombre="Roosevelt", capacidad_maxima=180, orden=3, linea_id=linea1.id, municipalidad_id=muni1.id),
            Estacion(nombre="Justo Rufino Barrios", capacidad_maxima=120, orden=4, linea_id=linea1.id, municipalidad_id=muni1.id),
            Estacion(nombre="Periférico", capacidad_maxima=160, orden=5, linea_id=linea1.id, municipalidad_id=muni1.id),
        ]
        estaciones_linea6 = [
            Estacion(nombre="San Juan", capacidad_maxima=100, orden=1, linea_id=linea6.id, municipalidad_id=muni1.id),
            Estacion(nombre="El Zapote", capacidad_maxima=130, orden=2, linea_id=linea6.id, municipalidad_id=muni1.id),
            Estacion(nombre="Petapa", capacidad_maxima=140, orden=3, linea_id=linea6.id, municipalidad_id=muni1.id),
        ]
        estaciones_linea12 = [
            Estacion(nombre="Parque Industrial", capacidad_maxima=90, orden=1, linea_id=linea12.id, municipalidad_id=muni1.id),
            Estacion(nombre="Roosevelt (L12)", capacidad_maxima=110, orden=2, linea_id=linea12.id, municipalidad_id=muni1.id),
            Estacion(nombre="San Miguel", capacidad_maxima=120, orden=3, linea_id=linea12.id, municipalidad_id=muni1.id),
        ]
        db.session.add_all(estaciones_linea1 + estaciones_linea6 + estaciones_linea12)
        db.session.commit()

        # 5. Parqueos (asociados a estaciones)
        parqueo_norte = Parqueo(ubicacion="Parqueo Norte", estacion_id=estaciones_linea1[0].id)
        parqueo_sur = Parqueo(ubicacion="Parqueo Sur", estacion_id=estaciones_linea1[0].id)
        parqueo_mixco = Parqueo(ubicacion="Parqueo Central Mixco", estacion_id=estaciones_linea12[0].id)
        db.session.add_all([parqueo_norte, parqueo_sur, parqueo_mixco])
        db.session.commit()

        # 6. Buses (asignando línea, piloto, parqueo)
        buses = [
            Bus(placa="101ABC", capacidad_max=80, capacidad_actual=0, estado="Disponible", linea_id=linea1.id, piloto_id=pilotos[0].id, parqueo_id=parqueo_norte.id),
            Bus(placa="102DEF", capacidad_max=80, capacidad_actual=0, estado="Disponible", linea_id=linea1.id, piloto_id=pilotos[1].id, parqueo_id=parqueo_sur.id),
            Bus(placa="103GHI", capacidad_max=80, capacidad_actual=0, estado="En ruta", linea_id=linea6.id, piloto_id=pilotos[2].id, parqueo_id=None),
            Bus(placa="104JKL", capacidad_max=80, capacidad_actual=0, estado="Disponible", linea_id=None, piloto_id=pilotos[3].id, parqueo_id=None),
            Bus(placa="105MNO", capacidad_max=80, capacidad_actual=0, estado="Mantenimiento", linea_id=None, piloto_id=pilotos[0].id, parqueo_id=parqueo_mixco.id),
        ]
        db.session.add_all(buses)
        db.session.commit()

        # 7. Distancias entre estaciones (solo para Línea 1)
        distancias = [
            Distancia(estacion_origen_id=estaciones_linea1[0].id, estacion_destino_id=estaciones_linea1[1].id, distancia_km=0.8, linea_id=linea1.id),
            Distancia(estacion_origen_id=estaciones_linea1[1].id, estacion_destino_id=estaciones_linea1[2].id, distancia_km=0.6, linea_id=linea1.id),
            Distancia(estacion_origen_id=estaciones_linea1[2].id, estacion_destino_id=estaciones_linea1[3].id, distancia_km=1.2, linea_id=linea1.id),
            Distancia(estacion_origen_id=estaciones_linea1[3].id, estacion_destino_id=estaciones_linea1[4].id, distancia_km=0.9, linea_id=linea1.id),
        ]
        db.session.add_all(distancias)
        db.session.commit()

        # 8. Accesos y Guardias (para la primera estación)
        acceso_norte = Acceso(nombre="Acceso Norte", estacion_id=estaciones_linea1[0].id)
        acceso_sur = Acceso(nombre="Acceso Sur", estacion_id=estaciones_linea1[0].id)
        db.session.add_all([acceso_norte, acceso_sur])
        db.session.flush()
        guardia1 = Guardia(nombre="Carlos López", turno="Matutino", acceso_id=acceso_norte.id)
        guardia2 = Guardia(nombre="Ana Gómez", turno="Vespertino", acceso_id=acceso_sur.id)
        db.session.add_all([guardia1, guardia2])
        db.session.commit()

        print("✅ Datos de ejemplo cargados exitosamente.")

if __name__ == "__main__":
    cargar_datos()