from app import app, db
from models import Municipalidad, Linea, Estacion, Piloto, Parqueo, Bus

with app.app_context():
    # Limpiar todo y recrear tablas
    db.drop_all()
    db.create_all()
    
    # 1. Municipalidad
    muni = Municipalidad(nombre="Municipalidad de Guatemala", direccion="Palacio Municipal")
    db.session.add(muni)
    db.session.commit()
    
    # 2. Línea
    linea = Linea(nombre="Línea 1", distancia_total=12.5, municipalidad_id=muni.id)
    db.session.add(linea)
    db.session.commit()
    
    # 3. Estación
    estacion = Estacion(nombre="Estación Central", capacidad_maxima=200, orden=1, linea_id=linea.id, municipalidad_id=muni.id)
    db.session.add(estacion)
    db.session.commit()
    
    # 4. Piloto
    piloto = Piloto(nombre="Juan Pérez", direccion="Zona 1", telefono="12345678", historial_educativo="Licencia tipo B")
    db.session.add(piloto)
    db.session.commit()
    
    # 5. Parqueos
    parqueo1 = Parqueo(ubicacion="Parqueo Norte", estacion_id=estacion.id)
    parqueo2 = Parqueo(ubicacion="Parqueo Sur", estacion_id=estacion.id)
    db.session.add_all([parqueo1, parqueo2])
    db.session.commit()
    
    # 6. Buses (asignando parqueo_id correctamente)
    bus1 = Bus(placa="P384JTK", capacidad_max=100, capacidad_actual=100, estado="Disponible",
               linea_id=linea.id, piloto_id=piloto.id, parqueo_id=parqueo2.id)
    bus2 = Bus(placa="BUS002", capacidad_max=80, capacidad_actual=20, estado="En ruta",
               linea_id=linea.id, piloto_id=piloto.id, parqueo_id=parqueo1.id)
    db.session.add_all([bus1, bus2])
    db.session.commit()
    
    print("Datos insertados correctamente")
    print("Usuario admin: admin / admin123")