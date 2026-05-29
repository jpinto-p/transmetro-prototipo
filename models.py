from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Municipalidad(db.Model):
    __tablename__ = 'municipalidades'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200))

class Linea(db.Model):
    __tablename__ = 'lineas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    distancia_total = db.Column(db.Float, default=0.0)
    municipalidad_id = db.Column(db.Integer, db.ForeignKey('municipalidades.id'))
    municipalidad = db.relationship('Municipalidad', backref='lineas')

class Estacion(db.Model):
    __tablename__ = 'estaciones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    capacidad_maxima = db.Column(db.Integer, nullable=False)
    orden = db.Column(db.Integer)
    linea_id = db.Column(db.Integer, db.ForeignKey('lineas.id'))
    municipalidad_id = db.Column(db.Integer, db.ForeignKey('municipalidades.id'))
    linea = db.relationship('Linea', backref='estaciones')
    municipalidad = db.relationship('Municipalidad', backref='estaciones')

class Piloto(db.Model):
    __tablename__ = 'pilotos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    historial_educativo = db.Column(db.Text)

class Parqueo(db.Model):
    __tablename__ = 'parqueos'
    id = db.Column(db.Integer, primary_key=True)
    ubicacion = db.Column(db.String(100))
    estacion_id = db.Column(db.Integer, db.ForeignKey('estaciones.id'))
    estacion = db.relationship('Estacion', backref='parqueos')
    # Relación uno a uno con Bus (usando la clave foránea que está en Bus)
    bus = db.relationship('Bus', backref='parqueo', uselist=False, foreign_keys='Bus.parqueo_id')

class Bus(db.Model):
    __tablename__ = 'buses'
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), unique=True, nullable=False)
    capacidad_max = db.Column(db.Integer, nullable=False)
    capacidad_actual = db.Column(db.Integer, default=0)
    estado = db.Column(db.String(20), default='Disponible')
    linea_id = db.Column(db.Integer, db.ForeignKey('lineas.id'), nullable=True)
    piloto_id = db.Column(db.Integer, db.ForeignKey('pilotos.id'), nullable=False)
    parqueo_id = db.Column(db.Integer, db.ForeignKey('parqueos.id'), nullable=True)
    linea = db.relationship('Linea', backref='buses')
    piloto = db.relationship('Piloto', backref='buses')
    # No definimos aquí la relación 'parqueo' porque ya está en Parqueo

class Acceso(db.Model):
    __tablename__ = 'accesos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    estacion_id = db.Column(db.Integer, db.ForeignKey('estaciones.id'))
    estacion = db.relationship('Estacion', backref='accesos')

class Guardia(db.Model):
    __tablename__ = 'guardias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    turno = db.Column(db.String(50))
    acceso_id = db.Column(db.Integer, db.ForeignKey('accesos.id'))
    acceso = db.relationship('Acceso', backref='guardias')

class Distancia(db.Model):
    __tablename__ = 'distancias'
    id = db.Column(db.Integer, primary_key=True)
    estacion_origen_id = db.Column(db.Integer, db.ForeignKey('estaciones.id'), nullable=False)
    estacion_destino_id = db.Column(db.Integer, db.ForeignKey('estaciones.id'), nullable=False)
    distancia_km = db.Column(db.Float, nullable=False)
    linea_id = db.Column(db.Integer, db.ForeignKey('lineas.id'), nullable=False)
    
    estacion_origen = db.relationship('Estacion', foreign_keys=[estacion_origen_id], backref='distancias_origen')
    estacion_destino = db.relationship('Estacion', foreign_keys=[estacion_destino_id], backref='distancias_destino')
    linea = db.relationship('Linea', backref='distancias')

class HistorialParqueo(db.Model):
    __tablename__ = 'historial_parqueos'
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    parqueo_anterior_id = db.Column(db.Integer, db.ForeignKey('parqueos.id'), nullable=True)
    parqueo_nuevo_id = db.Column(db.Integer, db.ForeignKey('parqueos.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    usuario = db.Column(db.String(100), nullable=False)
    
    bus = db.relationship('Bus', backref='historial_parqueos')
    parqueo_anterior = db.relationship('Parqueo', foreign_keys=[parqueo_anterior_id])
    parqueo_nuevo = db.relationship('Parqueo', foreign_keys=[parqueo_nuevo_id])