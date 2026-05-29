from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

class LineaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    distancia_total = FloatField('Distancia total (km)', validators=[Optional()])
    municipalidad_id = SelectField('Municipalidad', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

class EstacionForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    capacidad_maxima = IntegerField('Capacidad máxima', validators=[DataRequired()])
    orden = IntegerField('Orden en la línea', validators=[Optional()])
    linea_id = SelectField('Línea', coerce=int, validators=[DataRequired()])
    municipalidad_id = SelectField('Municipalidad', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

class BusForm(FlaskForm):
    placa = StringField('Placa', validators=[DataRequired()])
    capacidad_max = IntegerField('Capacidad máxima', validators=[DataRequired()])
    capacidad_actual = IntegerField('Capacidad actual', validators=[Optional()])
    estado = StringField('Estado', validators=[Optional()])
    linea_id = SelectField('Línea', coerce=int, validators=[Optional()])
    piloto_id = SelectField('Piloto', coerce=int, validators=[DataRequired()])
    parqueo_id = SelectField('Parqueo', coerce=int, validators=[Optional()])
    submit = SubmitField('Guardar')

class PilotoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[Optional()])
    telefono = StringField('Teléfono', validators=[Optional()])
    historial_educativo = StringField('Historial educativo', validators=[Optional()])
    submit = SubmitField('Guardar')

class DistanciaForm(FlaskForm):
    estacion_origen_id = SelectField('Estación origen', coerce=int, validators=[DataRequired()])
    estacion_destino_id = SelectField('Estación destino', coerce=int, validators=[DataRequired()])
    distancia_km = FloatField('Distancia (km)', validators=[DataRequired()])
    linea_id = SelectField('Línea', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

class CambioParqueoForm(FlaskForm):
    parqueo_id = SelectField('Nuevo parqueo', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Cambiar parqueo')

class ParqueoForm(FlaskForm):
    ubicacion = StringField('Ubicación', validators=[DataRequired()])
    estacion_id = SelectField('Estación', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')