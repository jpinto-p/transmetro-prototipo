from app import app, db
from models import Parqueo

with app.app_context():
    print("=== DIAGNÓSTICO DE RELACIÓN PARQUEO -> BUS ===")
    parqueos = Parqueo.query.all()
    if not parqueos:
        print("No hay parqueos en la BD.")
    else:
        for p in parqueos:
            print(f"Parqueo ID {p.id}: {p.ubicacion}")
            print(f"  - Tipo de p.bus: {type(p.bus)}")
            if p.bus is not None:
                if hasattr(p.bus, '__iter__') and not isinstance(p.bus, str):
                    print(f"  - ¡ERROR: p.bus es una lista con {len(p.bus)} elementos!")
                else:
                    print(f"  - OK: p.bus es objeto de tipo {type(p.bus)}")
                    try:
                        print(f"  - Placa: {p.bus.placa}")
                    except AttributeError:
                        print("  - El objeto no tiene atributo 'placa'")
            else:
                print("  - p.bus es None (Libre)")