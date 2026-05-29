# seed.py
from app import app, db
from models import (
    Municipalidad, Linea, Estacion, Distancia,
    Parqueo, Piloto, Bus
)
from werkzeug.security import generate_password_hash
from models import Admin

# Datos desde Gemini (adaptados)
municipalidad_info = {
    "nombre": "Municipalidad de Guatemala",
    "direccion": "21 Calle 6-77 Zona 1, Palacio Municipal",
}

lineas_info = [
    {"nombre": "Línea 1 (Centro Histórico)", "distancia_total_km": 8.1},
    {"nombre": "Línea 2 (Centro)", "distancia_total_km": 1.2},
    {"nombre": "Línea 6 (Eje Norte)", "distancia_total_km": 11.4},
    {"nombre": "Línea 7 (Eje Periférico)", "distancia_total_km": 15.3},
    {"nombre": "Línea 12 (Eje Sur)", "distancia_total_km": 13.9},
    {"nombre": "Línea 13 (Eje Suroriente)", "distancia_total_km": 10.2},
    {"nombre": "Línea 18 (Eje Norte)", "distancia_total_km": 9.5},
]

estaciones_info = [
    # Línea 1
    (1, "San Sebastián (L1)", 120),
    (1, "Colón (L1)", 100),
    (1, "Mercado Central (L1)", 200),
    (1, "Correos (L1)", 110),
    (1, "Beatas de Belén (L1)", 90),
    (1, "Paseo de las Letras", 150),
    (1, "Centro Cívico (L1)", 250),
    (1, "Sur 2", 100),
    (1, "Gómez Carrillo", 120),
    (1, "San Agustín", 90),
    (1, "Parque Centenario", 180),
    (1, "Capuchinas", 100),
    (1, "Tipografía", 130),
    # Línea 2
    (2, "San Sebastián (L2)", 120),
    (2, "Centro Cívico (L2)", 250),
    # Línea 6
    (6, "Proyectos", 150),
    (6, "Proyectos 4-4", 100),
    (6, "Cipresales", 110),
    (6, "Academia", 130),
    (6, "Centro Zona 6", 160),
    (6, "IGSS Zona 6", 200),
    (6, "Parroquia", 220),
    (6, "José Martí", 110),
    (6, "Santa Teresa", 90),
    (6, "Cerro del Carmen (L6)", 140),
    (6, "Mercado Central (L6)", 200),
    (6, "Correos (L6)", 110),
    (6, "Beatas de Belén (L6)", 90),
    (6, "Plaza Barrios (L6)", 350),
    # Línea 7
    (7, "USAC-Periférico", 400),
    (7, "Aguilar Batres", 300),
    (7, "Granai", 120),
    (7, "Rodolfo Robles", 110),
    (7, "Cejusa", 150),
    (7, "San Jorge", 130),
    (7, "Roosevelt", 280),
    (7, "San Juan", 280),
    (7, "Bethania", 180),
    (7, "Villa Linda", 160),
    (7, "Archivo General", 100),
    (7, "Cruz Roja", 120),
    (7, "San Juan de Dios", 150),
    (7, "Colón (L7)", 100),
    (7, "La Merced", 140),
    # Línea 12
    (12, "Centra Sur", 500),
    (12, "Monte María", 150),
    (12, "Javier", 160),
    (12, "Las Charcas", 220),
    (12, "El Carmen", 180),
    (12, "Reformita", 140),
    (12, "Mariscal", 150),
    (12, "Santa Cecilia", 130),
    (12, "El Trébol", 450),
    (12, "Bolívar", 200),
    (12, "Don Bosco", 160),
    (12, "Plaza Municipal", 180),
    (12, "El Calvario", 250),
    (12, "Plaza Barrios (L12)", 400),
    # Línea 13
    (13, "Plaza Berlín", 150),
    (13, "Hangares", 120),
    (13, "Fuerza Aérea", 110),
    (13, "Acueducto", 130),
    (13, "Montúfar", 160),
    (13, "Tívoli", 180),
    (13, "Industria", 140),
    (13, "Terminal", 300),
    (13, "Exposición", 150),
    (13, "4 Grados Sur", 160),
    (13, "Banco de Guatemala", 200),
    (13, "Plaza Barrios (L13)", 400),
    # Línea 18
    (18, "San Rafael", 250),
    (18, "Atlántida", 220),
    (18, "Victorias", 130),
    (18, "San Martín", 140),
    (18, "Santa Clara", 120),
    (18, "Cerro del Carmen (L18)", 140),
    (18, "FEGUA", 200),
    (18, "Plaza Barrios (L18)", 400),
]

distancias_info = [
    # Línea 1
    ("San Sebastián (L1)", "Colón (L1)", 0.6),
    ("Colón (L1)", "Mercado Central (L1)", 0.5),
    ("Mercado Central (L1)", "Correos (L1)", 0.4),
    ("Correos (L1)", "Beatas de Belén (L1)", 0.7),
    ("Beatas de Belén (L1)", "Paseo de las Letras", 0.8),
    ("Paseo de las Letras", "Centro Cívico (L1)", 0.5),
    ("Centro Cívico (L1)", "Sur 2", 0.6),
    ("Sur 2", "Gómez Carrillo", 0.8),
    ("Gómez Carrillo", "San Agustín", 0.5),
    ("San Agustín", "Parque Centenario", 0.7),
    ("Parque Centenario", "Capuchinas", 0.9),
    ("Capuchinas", "Tipografía", 1.1),
    # Línea 2
    ("San Sebastián (L2)", "Centro Cívico (L2)", 1.2),
    # Línea 6
    ("Proyectos", "Proyectos 4-4", 0.5),
    ("Proyectos 4-4", "Cipresales", 0.6),
    ("Cipresales", "Academia", 0.8),
    ("Academia", "Centro Zona 6", 1.1),
    ("Centro Zona 6", "IGSS Zona 6", 0.7),
    ("IGSS Zona 6", "Parroquia", 1.2),
    ("Parroquia", "José Martí", 0.9),
    ("José Martí", "Santa Teresa", 0.6),
    ("Santa Teresa", "Cerro del Carmen (L6)", 0.8),
    ("Cerro del Carmen (L6)", "Mercado Central (L6)", 1.4),
    ("Mercado Central (L6)", "Correos (L6)", 0.5),
    ("Correos (L6)", "Beatas de Belén (L6)", 0.7),
    ("Beatas de Belén (L6)", "Plaza Barrios (L6)", 1.6),
    # Línea 7
    ("USAC-Periférico", "Aguilar Batres", 1.8),
    ("Aguilar Batres", "Granai", 0.9),
    ("Granai", "Rodolfo Robles", 0.7),
    ("Rodolfo Robles", "Cejusa", 0.6),
    ("Cejusa", "San Jorge", 1.1),
    ("San Jorge", "Roosevelt", 1.3),
    ("Roosevelt", "San Juan", 0.8),
    ("San Juan", "Bethania", 1.5),
    ("Bethania", "Villa Linda", 1.2),
    ("Villa Linda", "Archivo General", 1.4),
    ("Archivo General", "Cruz Roja", 0.9),
    ("Cruz Roja", "San Juan de Dios", 0.7),
    ("San Juan de Dios", "Colón (L7)", 1.2),
    ("Colón (L7)", "La Merced", 0.6),
    # Línea 12
    ("Centra Sur", "Monte María", 1.5),
    ("Monte María", "Javier", 0.8),
    ("Javier", "Las Charcas", 1.2),
    ("Las Charcas", "El Carmen", 0.9),
    ("El Carmen", "Reformita", 0.7),
    ("Reformita", "Mariscal", 0.6),
    ("Mariscal", "Santa Cecilia", 1.1),
    ("Santa Cecilia", "El Trébol", 0.8),
    ("El Trébol", "Bolívar", 1.4),
    ("Bolívar", "Don Bosco", 1.2),
    ("Don Bosco", "Plaza Municipal", 0.9),
    ("Plaza Municipal", "El Calvario", 1.1),
    ("El Calvario", "Plaza Barrios (L12)", 0.9),
    # Línea 13
    ("Plaza Berlín", "Hangares", 1.3),
    ("Hangares", "Fuerza Aérea", 0.6),
    ("Fuerza Aérea", "Acueducto", 0.8),
    ("Acueducto", "Montúfar", 1.1),
    ("Montúfar", "Tívoli", 0.5),
    ("Tívoli", "Industria", 0.7),
    ("Industria", "Terminal", 1.4),
    ("Terminal", "Exposición", 0.9),
    ("Exposición", "4 Grados Sur", 0.6),
    ("4 Grados Sur", "Banco de Guatemala", 0.8),
    ("Banco de Guatemala", "Plaza Barrios (L13)", 1.5),
    # Línea 18
    ("San Rafael", "Atlántida", 2.1),
    ("Atlántida", "Victorias", 1.4),
    ("Victorias", "San Martín", 0.9),
    ("San Martín", "Santa Clara", 1.1),
    ("Santa Clara", "Cerro del Carmen (L18)", 1.5),
    ("Cerro del Carmen (L18)", "FEGUA", 1.3),
    ("FEGUA", "Plaza Barrios (L18)", 1.2),
]

parqueos_info = [
    {"ubicacion": "Centra Sur Base", "estacion_nombre": "Centra Sur"},
    {"ubicacion": "Predio San Rafael Norte", "estacion_nombre": "San Rafael"},
    {"ubicacion": "Parqueo Roosevelt Occidente", "estacion_nombre": "Roosevelt"},
    {"ubicacion": "Predio Usac Periférico", "estacion_nombre": "USAC-Periférico"},
    {"ubicacion": "Talleres Centrales Zona 1", "estacion_nombre": "Tipografía"},
    {"ubicacion": "Estación de Guardia Terminal", "estacion_nombre": "Terminal"},
]

pilotos_info = [
    {"nombre": "Carlos Humberto Marroquín Fuentes", "direccion": "5a avenida 12-45, Zona 12", "telefono": "4521-9876", "historial": "Licencia tipo A, Curso PMT de manejo defensivo, 8 años de experiencia"},
    {"nombre": "José Luis Hernández Chajón", "direccion": "14 calle A 3-12, Zona 7, Mixco", "telefono": "5214-8765", "historial": "Licencia tipo A, Certificación IRTRA transporte seguro, 6 años de experiencia"},
    {"nombre": "Juan Carlos Pérez Culajay", "direccion": "Lote 23, Manzana C, Ciudad Quetzal", "telefono": "3015-4421", "historial": "Licencia tipo B, Capacitación Intecap para Buses Articulados, 4 años de experiencia"},
    {"nombre": "Mynor René Estrada Gálvez", "direccion": "9a calle 2-50, Zona 1, Villa Nueva", "telefono": "4125-6321", "historial": "Licencia tipo A, Ex-piloto de rutas extraurbanas, 10 años de experiencia"},
    {"nombre": "Edgar Vinicio Teleguard Cruz", "direccion": "Avenida Petapa 35-12, Zona 21", "telefono": "5987-1425", "historial": "Licencia tipo A, Curso Primeros Auxilios Cruz Roja, 5 años de experiencia"},
    {"nombre": "Gustavo Adolfo Alonzo Godoy", "direccion": "3a calle 8-19, Zona 6", "telefono": "2451-8963", "historial": "Licencia tipo B, Bachiller Industrial, Capacitación interna Muni, 3 años de experiencia"},
    {"nombre": "Pedro Antonio Tux Chub", "direccion": "Km 15.5 Ruta al Atlántico, Zona 25", "telefono": "4752-1423", "historial": "Licencia tipo A, 12 años de experiencia en transporte pesado"},
    {"nombre": "Luis Fernando Chanchavac Pirir", "direccion": "6a avenida final, Zona 3", "telefono": "5142-3698", "historial": "Licencia tipo A, Curso de Relaciones Humanas e Inteligencia Emocional, 7 años de experiencia"},
    {"nombre": "Jorge Mario Valenzuela Lemus", "direccion": "Calle Real 4-11, San Miguel Petapa", "telefono": "3265-9874", "historial": "Licencia tipo B, Mecánica automotriz básica Intecap, 4 años de experiencia"},
    {"nombre": "Francisco Javier Chocoj Patzán", "direccion": "Diagonal 15, Col. Jardines de la Asunción, Zona 5", "telefono": "5562-4178", "historial": "Licencia tipo A, Certificación municipal de conductor élite, 9 años de experiencia"},
]

buses_info = [
    {"placa": "U451BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 12 (Eje Sur)", "piloto_nombre": "Carlos Humberto Marroquín Fuentes", "parqueo_ubicacion": "Centra Sur Base"},
    {"placa": "U125BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 12 (Eje Sur)", "piloto_nombre": "José Luis Hernández Chajón", "parqueo_ubicacion": "Centra Sur Base"},
    {"placa": "U896BRT", "capacidad_max": 90, "estado": "Disponible", "linea_nombre": "Línea 12 (Eje Sur)", "piloto_nombre": "Juan Carlos Pérez Culajay", "parqueo_ubicacion": "Centra Sur Base"},
    {"placa": "U235BRT", "capacidad_max": 90, "estado": "Mantenimiento", "linea_nombre": "Línea 12 (Eje Sur)", "piloto_nombre": "Mynor René Estrada Gálvez", "parqueo_ubicacion": "Centra Sur Base"},
    {"placa": "U741BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 7 (Eje Periférico)", "piloto_nombre": "Edgar Vinicio Teleguard Cruz", "parqueo_ubicacion": "Predio Usac Periférico"},
    {"placa": "U523BRT", "capacidad_max": 80, "estado": "En ruta", "linea_nombre": "Línea 7 (Eje Periférico)", "piloto_nombre": "Gustavo Adolfo Alonzo Godoy", "parqueo_ubicacion": "Parqueo Roosevelt Occidente"},
    {"placa": "U963BRT", "capacidad_max": 80, "estado": "Disponible", "linea_nombre": "Línea 7 (Eje Periférico)", "piloto_nombre": "Pedro Antonio Tux Chub", "parqueo_ubicacion": "Predio Usac Periférico"},
    {"placa": "U147BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 18 (Eje Norte)", "piloto_nombre": "Luis Fernando Chanchavac Pirir", "parqueo_ubicacion": "Predio San Rafael Norte"},
    {"placa": "U258BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 18 (Eje Norte)", "piloto_nombre": "Jorge Mario Valenzuela Lemus", "parqueo_ubicacion": "Predio San Rafael Norte"},
    {"placa": "U369BRT", "capacidad_max": 80, "estado": "Mantenimiento", "linea_nombre": "Línea 1 (Centro Histórico)", "piloto_nombre": "Francisco Javier Chocoj Patzán", "parqueo_ubicacion": "Talleres Centrales Zona 1"},
    {"placa": "U482BRT", "capacidad_max": 80, "estado": "En ruta", "linea_nombre": "Línea 1 (Centro Histórico)", "piloto_nombre": "Carlos Humberto Marroquín Fuentes", "parqueo_ubicacion": "Talleres Centrales Zona 1"},
    {"placa": "U753BRT", "capacidad_max": 80, "estado": "En ruta", "linea_nombre": "Línea 2 (Centro)", "piloto_nombre": "José Luis Hernández Chajón", "parqueo_ubicacion": "Talleres Centrales Zona 1"},
    {"placa": "U951BRT", "capacidad_max": 90, "estado": "Disponible", "linea_nombre": "Línea 6 (Eje Norte)", "piloto_nombre": "Juan Carlos Pérez Culajay", "parqueo_ubicacion": "Talleres Centrales Zona 1"},
    {"placa": "U357BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 6 (Eje Norte)", "piloto_nombre": "Mynor René Estrada Gálvez", "parqueo_ubicacion": "Estación de Guardia Terminal"},
    {"placa": "U159BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 13 (Eje Suroriente)", "piloto_nombre": "Edgar Vinicio Teleguard Cruz", "parqueo_ubicacion": "Estación de Guardia Terminal"},
    {"placa": "U852BRT", "capacidad_max": 90, "estado": "Disponible", "linea_nombre": "Línea 13 (Eje Suroriente)", "piloto_nombre": "Gustavo Adolfo Alonzo Godoy", "parqueo_ubicacion": "Estación de Guardia Terminal"},
    {"placa": "U426BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 12 (Eje Sur)", "piloto_nombre": "Pedro Antonio Tux Chub", "parqueo_ubicacion": "Centra Sur Base"},
    {"placa": "U784BRT", "capacidad_max": 80, "estado": "En ruta", "linea_nombre": "Línea 7 (Eje Periférico)", "piloto_nombre": "Luis Fernando Chanchavac Pirir", "parqueo_ubicacion": "Parqueo Roosevelt Occidente"},
    {"placa": "U139BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 18 (Eje Norte)", "piloto_nombre": "Jorge Mario Valenzuela Lemus", "parqueo_ubicacion": "Predio San Rafael Norte"},
    {"placa": "U642BRT", "capacidad_max": 90, "estado": "Mantenimiento", "linea_nombre": "Línea 13 (Eje Suroriente)", "piloto_nombre": "Francisco Javier Chocoj Patzán", "parqueo_ubicacion": "Estación de Guardia Terminal"},
    {"placa": "U201BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 12 (Eje Sur)", "piloto_nombre": "Carlos Humberto Marroquín Fuentes", "parqueo_ubicacion": "Centra Sur Base"},
    {"placa": "U202BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 12 (Eje Sur)", "piloto_nombre": "José Luis Hernández Chajón", "parqueo_ubicacion": "Centra Sur Base"},
    {"placa": "U203BRT", "capacidad_max": 80, "estado": "Disponible", "linea_nombre": "Línea 7 (Eje Periférico)", "piloto_nombre": "Juan Carlos Pérez Culajay", "parqueo_ubicacion": "Predio Usac Periférico"},
    {"placa": "U204BRT", "capacidad_max": 80, "estado": "En ruta", "linea_nombre": "Línea 7 (Eje Periférico)", "piloto_nombre": "Mynor René Estrada Gálvez", "parqueo_ubicacion": "Parqueo Roosevelt Occidente"},
    {"placa": "U205BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 6 (Eje Norte)", "piloto_nombre": "Edgar Vinicio Teleguard Cruz", "parqueo_ubicacion": "Estación de Guardia Terminal"},
    {"placa": "U206BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 6 (Eje Norte)", "piloto_nombre": "Gustavo Adolfo Alonzo Godoy", "parqueo_ubicacion": "Talleres Centrales Zona 1"},
    {"placa": "U207BRT", "capacidad_max": 90, "estado": "Disponible", "linea_nombre": "Línea 18 (Eje Norte)", "piloto_nombre": "Pedro Antonio Tux Chub", "parqueo_ubicacion": "Predio San Rafael Norte"},
    {"placa": "U208BRT", "capacidad_max": 80, "estado": "En ruta", "linea_nombre": "Línea 1 (Centro Histórico)", "piloto_nombre": "Luis Fernando Chanchavac Pirir", "parqueo_ubicacion": "Talleres Centrales Zona 1"},
    {"placa": "U209BRT", "capacidad_max": 80, "estado": "En ruta", "linea_nombre": "Línea 2 (Centro)", "piloto_nombre": "Jorge Mario Valenzuela Lemus", "parqueo_ubicacion": "Talleres Centrales Zona 1"},
    {"placa": "U210BRT", "capacidad_max": 90, "estado": "En ruta", "linea_nombre": "Línea 13 (Eje Suroriente)", "piloto_nombre": "Francisco Javier Chocoj Patzán", "parqueo_ubicacion": "Estación de Guardia Terminal"},
]

with app.app_context():
    # Opcional: borrar todo para empezar de cero (descomentar si quieres limpiar)
    # db.drop_all()
    # db.create_all()

    # 1. Administrador
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin', password=generate_password_hash('admin123'))
        db.session.add(admin)
        print(" Administrador creado (admin / admin123)")

    # 2. Municipalidad (solo una)
    muni = Municipalidad.query.first()
    if not muni:
        muni = Municipalidad(**municipalidad_info)
        db.session.add(muni)
        db.session.commit()
        print(" Municipalidad creada")

    # 3. Líneas
    lineas_obj = {}
    for info in lineas_info:
        linea = Linea.query.filter_by(nombre=info["nombre"]).first()
        if not linea:
            linea = Linea(
                nombre=info["nombre"],
                distancia_total=info["distancia_total_km"],
                municipalidad_id=muni.id
            )
            db.session.add(linea)
            db.session.flush()
        lineas_obj[info["nombre"]] = linea
    db.session.commit()
    print(" Líneas creadas")

    # 4. Estaciones y distancias
    # Insertar estaciones en orden y guardar sus IDs reales
    estacion_id_map = {}
    for (linea_id_ref, nombre, cap) in estaciones_info:
        # Buscar línea por nombre (no por ID del JSON)
        linea_objeto = None
        for ln in lineas_info:
            if ln["nombre"].startswith(f"Línea {linea_id_ref}"):
                linea_objeto = lineas_obj[ln["nombre"]]
                break
        if not linea_objeto:
            print(f"Línea con ref {linea_id_ref} no encontrada para estación {nombre}")
            continue
        estacion = Estacion.query.filter_by(nombre=nombre).first()
        if not estacion:
            estacion = Estacion(
                nombre=nombre,
                capacidad_maxima=cap,
                orden=0,  # se actualizará después
                linea_id=linea_objeto.id,
                municipalidad_id=muni.id
            )
            db.session.add(estacion)
            db.session.flush()
        estacion_id_map[nombre] = estacion.id
    # Recalcular orden dentro de cada línea
    for linea_objeto in lineas_obj.values():
        estaciones_linea = Estacion.query.filter_by(linea_id=linea_objeto.id).order_by(Estacion.id).all()
        for idx, e in enumerate(estaciones_linea, start=1):
            e.orden = idx
    db.session.commit()
    print(" Estaciones creadas")

    # 5. Distancias (usando nombres de estación)
    for (origen_nom, destino_nom, dist_km) in distancias_info:
        origen_id = estacion_id_map.get(origen_nom)
        destino_id = estacion_id_map.get(destino_nom)
        if origen_id and destino_id:
            # Obtener línea a partir de cualquiera de las dos estaciones
            est_origen = Estacion.query.get(origen_id)
            linea_id = est_origen.linea_id
            # Evitar duplicados
            if not Distancia.query.filter_by(estacion_origen_id=origen_id, estacion_destino_id=destino_id).first():
                dist = Distancia(
                    estacion_origen_id=origen_id,
                    estacion_destino_id=destino_id,
                    distancia_km=dist_km,
                    linea_id=linea_id
                )
                db.session.add(dist)
    db.session.commit()
    print(" Distancias creadas")

    # 6. Parqueos (asociar a estación por nombre)
    for p in parqueos_info:
        estacion = Estacion.query.filter_by(nombre=p["estacion_nombre"]).first()
        if not estacion:
            print(f" Estación '{p['estacion_nombre']}' no encontrada para parqueo '{p['ubicacion']}'")
            continue
        parqueo = Parqueo.query.filter_by(ubicacion=p["ubicacion"]).first()
        if not parqueo:
            parqueo = Parqueo(
                ubicacion=p["ubicacion"],
                estacion_id=estacion.id
            )
            db.session.add(parqueo)
    db.session.commit()
    print(" Parqueos creados")

    # 7. Pilotos
    pilotos_obj = {}
    for p in pilotos_info:
        piloto = Piloto.query.filter_by(nombre=p["nombre"]).first()
        if not piloto:
            piloto = Piloto(
                nombre=p["nombre"],
                direccion=p["direccion"],
                telefono=p["telefono"],
                historial_educativo=p["historial"]
            )
            db.session.add(piloto)
            db.session.flush()
        pilotos_obj[p["nombre"]] = piloto
    db.session.commit()
    print("Pilotos creados")

    # 8. Buses
    for b in buses_info:
        linea = Linea.query.filter_by(nombre=b["linea_nombre"]).first()
        piloto = pilotos_obj.get(b["piloto_nombre"])
        parqueo = Parqueo.query.filter_by(ubicacion=b["parqueo_ubicacion"]).first()
        if not linea or not piloto or not parqueo:
            print(f" No se pudo crear bus {b['placa']}: falta línea, piloto o parqueo")
            continue
        bus = Bus.query.filter_by(placa=b["placa"]).first()
        if not bus:
            bus = Bus(
                placa=b["placa"],
                capacidad_max=b["capacidad_max"],
                capacidad_actual=0,
                estado=b["estado"],
                linea_id=linea.id,
                piloto_id=piloto.id,
                parqueo_id=parqueo.id
            )
            db.session.add(bus)
    db.session.commit()
    print(" Buses creados")

    print("\n ¡Base de datos poblada exitosamente con datos reales del Transmetro!")
    print("Credenciales de administrador: admin / admin123")