# reset_guardias.py
from app import app, db
from models import Acceso, Guardia

with app.app_context():
    # Eliminar todos los guardias y accesos existentes
    db.session.query(Guardia).delete()
    db.session.query(Acceso).delete()
    db.session.commit()
    print("✅ Todos los guardias y accesos han sido eliminados.")