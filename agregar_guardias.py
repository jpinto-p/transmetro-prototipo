# agregar_guardias_limpios.py
from app import app, db
from models import Estacion, Acceso, Guardia

# Nombres de guardias para alternar (puedes añadir más)
nombres_guardias = [
    "Carlos López", "Ana Gómez", "Luis Pérez", "María Rodríguez",
    "José Martínez", "Laura García", "Pedro Hernández", "Sofía Díaz"
]

def obtener_guardia_nombre(idx):
    return nombres_guardias[idx % len(nombres_guardias)]

with app.app_context():
    estaciones = Estacion.query.all()
    if not estaciones:
        print("⚠️ No hay estaciones. Ejecuta seed.py primero.")
    else:
        # Contador para distribuir guardias
        cont = 0
        for estacion in estaciones:
            # Acceso Norte
            acceso_norte = Acceso.query.filter_by(nombre=f"{estacion.nombre} - Norte", estacion_id=estacion.id).first()
            if not acceso_norte:
                acceso_norte = Acceso(nombre=f"{estacion.nombre} - Norte", estacion_id=estacion.id)
                db.session.add(acceso_norte)
                db.session.flush()
                print(f"✅ Acceso creado: {acceso_norte.nombre}")
            # Guardia para acceso Norte
            nombre_guardia = obtener_guardia_nombre(cont)
            guardia_norte = Guardia.query.filter_by(acceso_id=acceso_norte.id).first()
            if not guardia_norte:
                guardia_norte = Guardia(nombre=nombre_guardia, turno="Matutino", acceso_id=acceso_norte.id)
                db.session.add(guardia_norte)
                print(f"   👮 Guardia {nombre_guardia} (Matutino) asignado a {acceso_norte.nombre}")
            cont += 1

            # Acceso Sur
            acceso_sur = Acceso.query.filter_by(nombre=f"{estacion.nombre} - Sur", estacion_id=estacion.id).first()
            if not acceso_sur:
                acceso_sur = Acceso(nombre=f"{estacion.nombre} - Sur", estacion_id=estacion.id)
                db.session.add(acceso_sur)
                db.session.flush()
                print(f"✅ Acceso creado: {acceso_sur.nombre}")
            # Guardia para acceso Sur (turno vespertino)
            nombre_guardia = obtener_guardia_nombre(cont)
            guardia_sur = Guardia.query.filter_by(acceso_id=acceso_sur.id).first()
            if not guardia_sur:
                guardia_sur = Guardia(nombre=nombre_guardia, turno="Vespertino", acceso_id=acceso_sur.id)
                db.session.add(guardia_sur)
                print(f"   👮 Guardia {nombre_guardia} (Vespertino) asignado a {acceso_sur.nombre}")
            cont += 1

            # Opcional: para estaciones con alta capacidad (> 250) añadir un acceso extra con guardia nocturno
            if estacion.capacidad_maxima > 250:
                acceso_extra = Acceso.query.filter_by(nombre=f"{estacion.nombre} - Extra", estacion_id=estacion.id).first()
                if not acceso_extra:
                    acceso_extra = Acceso(nombre=f"{estacion.nombre} - Extra", estacion_id=estacion.id)
                    db.session.add(acceso_extra)
                    db.session.flush()
                    print(f"✅ Acceso extra creado: {acceso_extra.nombre}")
                nombre_guardia = obtener_guardia_nombre(cont)
                guardia_extra = Guardia.query.filter_by(acceso_id=acceso_extra.id).first()
                if not guardia_extra:
                    guardia_extra = Guardia(nombre=nombre_guardia, turno="Nocturno", acceso_id=acceso_extra.id)
                    db.session.add(guardia_extra)
                    print(f"   👮 Guardia {nombre_guardia} (Nocturno) asignado a {acceso_extra.nombre}")
                cont += 1

        db.session.commit()
        print("\n🎉 Proceso completado. Todos los accesos y guardias están limpios.")