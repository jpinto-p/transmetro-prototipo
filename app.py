import os
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Admin, Municipalidad, Linea, Estacion, Bus, Piloto, Parqueo, Acceso, Guardia, Distancia, HistorialParqueo
from forms import LineaForm, EstacionForm, BusForm, PilotoForm, DistanciaForm, CambioParqueoForm, ParqueoForm
from random import randint, random
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-para-prototipo'

# Configuración de la base de datos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db_path = os.path.join(BASE_DIR, 'transmetro.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear tablas y usuario administrador (solo si no existen)
with app.app_context():
    db.create_all()
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin', password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario administrador creado")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# ========== RUTAS PRINCIPALES ==========
@app.route('/')
def index():
    lineas = Linea.query.all()
    return render_template('index.html', lineas=lineas)

@app.route('/test')
def test():
    return "<h1>Funciona</h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    total_lineas = Linea.query.count()
    total_estaciones = Estacion.query.count()
    total_buses = Bus.query.count()
    total_pilotos = Piloto.query.count()
    estaciones = Estacion.query.all()
    estaciones_nombres = [e.nombre for e in estaciones]
    estaciones_capacidades = [e.capacidad_maxima for e in estaciones]
    lineas = Linea.query.all()
    return render_template('dashboard.html',
                           total_lineas=total_lineas,
                           total_estaciones=total_estaciones,
                           total_buses=total_buses,
                           total_pilotos=total_pilotos,
                           estaciones_nombres=estaciones_nombres,
                           estaciones_capacidades=estaciones_capacidades,
                           lineas=lineas)

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

# ========== MONITOREO EN TIEMPO REAL (ESTACIONES) ==========
@app.route('/monitoreo')
@login_required
def monitoreo():
    estaciones = Estacion.query.all()
    return render_template('monitoreo.html', estaciones=estaciones)

@app.route('/api/aforo')
@login_required
def api_aforo():
    data = {}
    for e in Estacion.query.all():
        maximo = e.capacidad_maxima
        if maximo > 0:
            data[e.id] = randint(0, int(maximo * 1.8))
        else:
            data[e.id] = 0
    return jsonify(data)

# ========== MONITOREO EN TIEMPO REAL (BUSES) ==========
@app.route('/monitoreo_buses')
@login_required
def monitoreo_buses():
    buses = Bus.query.all()
    return render_template('monitoreo_buses.html', buses=buses)

@app.route('/api/aforo_buses')
@login_required
def api_aforo_buses():
    data = {}
    for b in Bus.query.all():
        data[b.id] = randint(0, b.capacidad_max)
    return jsonify(data)

# ========== CONECTIVIDAD SIMULADA (REQ-006) ==========
@app.route('/api/conectividad')
@login_required
def api_conectividad():
    data = {}
    for e in Estacion.query.all():
        data[e.id] = random() < 0.8
    return jsonify(data)

# ========== CRUD LÍNEAS ==========
@app.route('/lineas')
@login_required
def listar_lineas():
    lineas = Linea.query.all()
    return render_template('listar_lineas.html', lineas=lineas)

@app.route('/lineas/agregar', methods=['GET', 'POST'])
@login_required
def agregar_linea():
    form = LineaForm()
    form.municipalidad_id.choices = [(m.id, m.nombre) for m in Municipalidad.query.all()]
    if form.validate_on_submit():
        nueva = Linea(
            nombre=form.nombre.data,
            distancia_total=form.distancia_total.data or 0.0,
            municipalidad_id=form.municipalidad_id.data
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Línea agregada correctamente')
        return redirect(url_for('listar_lineas'))
    return render_template('agregar_linea.html', form=form)

@app.route('/lineas/editar/<int:linea_id>', methods=['GET', 'POST'])
@login_required
def editar_linea(linea_id):
    linea = Linea.query.get_or_404(linea_id)
    form = LineaForm(obj=linea)
    form.municipalidad_id.choices = [(m.id, m.nombre) for m in Municipalidad.query.all()]
    if form.validate_on_submit():
        linea.nombre = form.nombre.data
        linea.distancia_total = form.distancia_total.data or 0.0
        linea.municipalidad_id = form.municipalidad_id.data
        db.session.commit()
        flash('Línea actualizada correctamente', 'success')
        return redirect(url_for('listar_lineas'))
    return render_template('editar_linea.html', form=form, linea=linea)

@app.route('/lineas/eliminar/<int:linea_id>')
@login_required
def eliminar_linea(linea_id):
    linea = Linea.query.get_or_404(linea_id)
    db.session.delete(linea)
    db.session.commit()
    flash('Línea eliminada correctamente', 'success')
    return redirect(url_for('listar_lineas'))

# ========== CRUD ESTACIONES ==========
@app.route('/estaciones')
@login_required
def listar_estaciones():
    estaciones = Estacion.query.all()
    return render_template('listar_estaciones.html', estaciones=estaciones)

@app.route('/estaciones/agregar', methods=['GET', 'POST'])
@login_required
def agregar_estacion():
    form = EstacionForm()
    form.linea_id.choices = [(l.id, l.nombre) for l in Linea.query.all()]
    form.municipalidad_id.choices = [(m.id, m.nombre) for m in Municipalidad.query.all()]
    if form.validate_on_submit():
        nueva = Estacion(
            nombre=form.nombre.data,
            capacidad_maxima=form.capacidad_maxima.data,
            orden=form.orden.data or 0,
            linea_id=form.linea_id.data,
            municipalidad_id=form.municipalidad_id.data
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Estación agregada correctamente')
        return redirect(url_for('listar_estaciones'))
    return render_template('agregar_estacion.html', form=form)

@app.route('/estaciones/editar/<int:estacion_id>', methods=['GET', 'POST'])
@login_required
def editar_estacion(estacion_id):
    estacion = Estacion.query.get_or_404(estacion_id)
    form = EstacionForm(obj=estacion)
    form.linea_id.choices = [(l.id, l.nombre) for l in Linea.query.all()]
    form.municipalidad_id.choices = [(m.id, m.nombre) for m in Municipalidad.query.all()]
    if form.validate_on_submit():
        estacion.nombre = form.nombre.data
        estacion.capacidad_maxima = form.capacidad_maxima.data
        estacion.orden = form.orden.data or 0
        estacion.linea_id = form.linea_id.data
        estacion.municipalidad_id = form.municipalidad_id.data
        db.session.commit()
        flash('Estación actualizada correctamente', 'success')
        return redirect(url_for('listar_estaciones'))
    return render_template('editar_estacion.html', form=form, estacion=estacion)

@app.route('/estaciones/eliminar/<int:estacion_id>')
@login_required
def eliminar_estacion(estacion_id):
    estacion = Estacion.query.get_or_404(estacion_id)
    db.session.delete(estacion)
    db.session.commit()
    flash('Estación eliminada correctamente', 'success')
    return redirect(url_for('listar_estaciones'))

# ========== CRUD BUSES ==========
@app.route('/buses')
@login_required
def listar_buses():
    buses = Bus.query.all()
    return render_template('listar_buses.html', buses=buses)

@app.route('/buses/agregar', methods=['GET', 'POST'])
@login_required
def agregar_bus():
    form = BusForm()
    form.linea_id.choices = [(l.id, l.nombre) for l in Linea.query.all()]
    form.linea_id.choices.insert(0, (0, '-- Sin línea --'))
    form.piloto_id.choices = [(p.id, p.nombre) for p in Piloto.query.all()]
    form.parqueo_id.choices = [(pq.id, pq.ubicacion) for pq in Parqueo.query.all()]
    form.parqueo_id.choices.insert(0, (0, '-- Sin parqueo --'))
    if form.validate_on_submit():
        nuevo = Bus(
            placa=form.placa.data,
            capacidad_max=form.capacidad_max.data,
            capacidad_actual=form.capacidad_actual.data or 0,
            estado=form.estado.data or 'Disponible',
            linea_id=form.linea_id.data if form.linea_id.data != 0 else None,
            piloto_id=form.piloto_id.data,
            parqueo_id=form.parqueo_id.data if form.parqueo_id.data != 0 else None
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Bus agregado correctamente')
        return redirect(url_for('listar_buses'))
    return render_template('agregar_bus.html', form=form)

@app.route('/buses/editar/<int:bus_id>', methods=['GET', 'POST'])
@login_required
def editar_bus(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    form = BusForm(obj=bus)
    form.linea_id.choices = [(l.id, l.nombre) for l in Linea.query.all()]
    form.linea_id.choices.insert(0, (0, '-- Sin línea --'))
    form.piloto_id.choices = [(p.id, p.nombre) for p in Piloto.query.all()]
    form.parqueo_id.choices = [(pq.id, pq.ubicacion) for pq in Parqueo.query.all()]
    form.parqueo_id.choices.insert(0, (0, '-- Sin parqueo --'))
    if form.validate_on_submit():
        bus.placa = form.placa.data
        bus.capacidad_max = form.capacidad_max.data
        bus.capacidad_actual = form.capacidad_actual.data or 0
        bus.estado = form.estado.data or 'Disponible'
        bus.linea_id = form.linea_id.data if form.linea_id.data != 0 else None
        bus.piloto_id = form.piloto_id.data
        bus.parqueo_id = form.parqueo_id.data if form.parqueo_id.data != 0 else None
        db.session.commit()
        flash('Bus actualizado correctamente', 'success')
        return redirect(url_for('listar_buses'))
    return render_template('editar_bus.html', form=form, bus=bus)

@app.route('/buses/eliminar/<int:bus_id>')
@login_required
def eliminar_bus(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    db.session.delete(bus)
    db.session.commit()
    flash('Bus eliminado correctamente', 'success')
    return redirect(url_for('listar_buses'))

# ========== VERIFICAR OCUPACIÓN (GET) ==========
@app.route('/buses/verificar/<int:bus_id>')
@login_required
def verificar_ocupacion_bus(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    porcentaje = (bus.capacidad_actual / bus.capacidad_max) * 100 if bus.capacidad_max > 0 else 0
    if porcentaje < 25:
        flash(f'⚠️ El bus {bus.placa} tiene menos del 25% de capacidad ({porcentaje:.1f}%). Debe esperar 5 minutos en cada estación.', 'warning')
    else:
        flash(f'✅ El bus {bus.placa} tiene {porcentaje:.1f}% de capacidad. Continúa normal.', 'success')
    return redirect(url_for('listar_buses'))

# ========== CRUD PILOTOS ==========
@app.route('/pilotos')
@login_required
def listar_pilotos():
    pilotos = Piloto.query.all()
    return render_template('listar_pilotos.html', pilotos=pilotos)

@app.route('/pilotos/agregar', methods=['GET', 'POST'])
@login_required
def agregar_piloto():
    form = PilotoForm()
    if form.validate_on_submit():
        nuevo = Piloto(
            nombre=form.nombre.data,
            direccion=form.direccion.data,
            telefono=form.telefono.data,
            historial_educativo=form.historial_educativo.data
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Piloto agregado correctamente')
        return redirect(url_for('listar_pilotos'))
    return render_template('agregar_piloto.html', form=form)

@app.route('/pilotos/editar/<int:piloto_id>', methods=['GET', 'POST'])
@login_required
def editar_piloto(piloto_id):
    piloto = Piloto.query.get_or_404(piloto_id)
    form = PilotoForm(obj=piloto)
    if form.validate_on_submit():
        piloto.nombre = form.nombre.data
        piloto.direccion = form.direccion.data
        piloto.telefono = form.telefono.data
        piloto.historial_educativo = form.historial_educativo.data
        db.session.commit()
        flash('Piloto actualizado correctamente', 'success')
        return redirect(url_for('listar_pilotos'))
    return render_template('editar_piloto.html', form=form, piloto=piloto)

@app.route('/pilotos/eliminar/<int:piloto_id>')
@login_required
def eliminar_piloto(piloto_id):
    piloto = Piloto.query.get_or_404(piloto_id)
    for bus in piloto.buses:
        bus.piloto_id = None
    db.session.delete(piloto)
    db.session.commit()
    flash('Piloto eliminado correctamente', 'success')
    return redirect(url_for('listar_pilotos'))

# ========== CRUD PARQUEOS ==========
@app.route('/parqueos')
@login_required
def listar_parqueos():
    parqueos = Parqueo.query.options(joinedload(Parqueo.bus)).all()
    return render_template('listar_parqueos.html', parqueos=parqueos)

@app.route('/parqueos/agregar', methods=['GET', 'POST'])
@login_required
def agregar_parqueo():
    form = ParqueoForm()
    form.estacion_id.choices = [(e.id, e.nombre) for e in Estacion.query.all()]
    if form.validate_on_submit():
        nuevo = Parqueo(
            ubicacion=form.ubicacion.data,
            estacion_id=form.estacion_id.data
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Parqueo agregado correctamente', 'success')
        return redirect(url_for('listar_parqueos'))
    return render_template('agregar_parqueo.html', form=form)

@app.route('/parqueos/editar/<int:parqueo_id>', methods=['GET', 'POST'])
@login_required
def editar_parqueo(parqueo_id):
    parqueo = Parqueo.query.get_or_404(parqueo_id)
    form = ParqueoForm(obj=parqueo)
    form.estacion_id.choices = [(e.id, e.nombre) for e in Estacion.query.all()]
    if form.validate_on_submit():
        parqueo.ubicacion = form.ubicacion.data
        parqueo.estacion_id = form.estacion_id.data
        db.session.commit()
        flash('Parqueo actualizado correctamente', 'success')
        return redirect(url_for('listar_parqueos'))
    return render_template('editar_parqueo.html', form=form, parqueo=parqueo)

@app.route('/parqueos/eliminar/<int:parqueo_id>')
@login_required
def eliminar_parqueo(parqueo_id):
    parqueo = Parqueo.query.get_or_404(parqueo_id)
    if parqueo.bus:
        flash('No se puede eliminar porque está asignado a un bus', 'danger')
    else:
        db.session.delete(parqueo)
        db.session.commit()
        flash('Parqueo eliminado correctamente', 'success')
    return redirect(url_for('listar_parqueos'))

# ========== REQ-009: ACCESOS POR LÍNEA ==========
@app.route('/accesos_por_linea', methods=['GET', 'POST'])
@login_required
def accesos_por_linea():
    lineas = Linea.query.all()
    accesos = []
    linea_seleccionada = None
    if request.method == 'POST':
        linea_id = request.form.get('linea_id')
        if linea_id:
            linea_seleccionada = Linea.query.get(int(linea_id))
            for estacion in linea_seleccionada.estaciones:
                for acceso in estacion.accesos:
                    accesos.append({
                        'estacion': estacion.nombre,
                        'acceso': acceso.nombre,
                        'guardias': [g.nombre for g in acceso.guardias]
                    })
    return render_template('accesos_por_linea.html', lineas=lineas, accesos=accesos, linea_seleccionada=linea_seleccionada)

# ========== REQ-011 y REQ-012: DISTANCIAS ENTRE ESTACIONES ==========
@app.route('/distancias')
@login_required
def listar_distancias():
    distancias = Distancia.query.all()
    return render_template('listar_distancias.html', distancias=distancias)

@app.route('/distancias/agregar', methods=['GET', 'POST'])
@login_required
def agregar_distancia():
    form = DistanciaForm()
    form.estacion_origen_id.choices = [(e.id, e.nombre) for e in Estacion.query.all()]
    form.estacion_destino_id.choices = [(e.id, e.nombre) for e in Estacion.query.all()]
    form.linea_id.choices = [(l.id, l.nombre) for l in Linea.query.all()]
    if form.validate_on_submit():
        nueva = Distancia(
            estacion_origen_id=form.estacion_origen_id.data,
            estacion_destino_id=form.estacion_destino_id.data,
            distancia_km=form.distancia_km.data,
            linea_id=form.linea_id.data
        )
        db.session.add(nueva)
        db.session.commit()
        linea = Linea.query.get(form.linea_id.data)
        total = db.session.query(db.func.sum(Distancia.distancia_km)).filter(Distancia.linea_id == linea.id).scalar() or 0
        linea.distancia_total = total
        db.session.commit()
        flash('Distancia agregada correctamente', 'success')
        return redirect(url_for('listar_distancias'))
    return render_template('agregar_distancia.html', form=form)

@app.route('/distancias/eliminar/<int:id>')
@login_required
def eliminar_distancia(id):
    distancia = Distancia.query.get_or_404(id)
    linea_id = distancia.linea_id
    db.session.delete(distancia)
    db.session.commit()
    linea = Linea.query.get(linea_id)
    total = db.session.query(db.func.sum(Distancia.distancia_km)).filter(Distancia.linea_id == linea.id).scalar() or 0
    linea.distancia_total = total
    db.session.commit()
    flash('Distancia eliminada', 'success')
    return redirect(url_for('listar_distancias'))

# ========== REQ-014: CAMBIO DE PARQUEO CON TRAZABILIDAD ==========
@app.route('/cambiar_parqueo/<int:bus_id>', methods=['GET', 'POST'])
@login_required
def cambiar_parqueo(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    form = CambioParqueoForm()
    form.parqueo_id.choices = [(p.id, p.ubicacion) for p in Parqueo.query.all()] + [(0, '-- Sin parqueo --')]
    if form.validate_on_submit():
        nuevo_parqueo_id = form.parqueo_id.data if form.parqueo_id.data != 0 else None
        anterior_id = bus.parqueo_id
        historial = HistorialParqueo(
            bus_id=bus.id,
            parqueo_anterior_id=anterior_id,
            parqueo_nuevo_id=nuevo_parqueo_id,
            usuario=current_user.username
        )
        db.session.add(historial)
        bus.parqueo_id = nuevo_parqueo_id
        db.session.commit()
        flash(f'Parqueo del bus {bus.placa} cambiado exitosamente', 'success')
        return redirect(url_for('listar_buses'))
    return render_template('cambiar_parqueo.html', bus=bus, form=form)

@app.route('/historial_parqueos/<int:bus_id>')
@login_required
def historial_parqueos(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    historial = HistorialParqueo.query.filter_by(bus_id=bus.id).order_by(HistorialParqueo.fecha.desc()).all()
    return render_template('historial_parqueos.html', bus=bus, historial=historial)

# ========== DETALLE DE LÍNEA ==========
@app.route('/linea/<int:linea_id>')
@login_required
def detalle_linea(linea_id):
    linea = Linea.query.get_or_404(linea_id)
    estaciones = Estacion.query.filter_by(linea_id=linea.id).order_by(Estacion.orden).all()
    buses = Bus.query.filter_by(linea_id=linea.id).all()
    return render_template('detalle_linea.html', linea=linea, estaciones=estaciones, buses=buses)

if __name__ == '__main__':
    app.run(debug=True)
