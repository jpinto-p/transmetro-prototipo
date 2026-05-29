from sqlalchemy import inspect
from app import db
from models import Bus, Parqueo

inspector = inspect(db.engine)
print("Tablas:", inspector.get_table_names())
print("Relación Bus -> parqueo:", Bus.parqueo)
print("Relación Parqueo -> bus:", Parqueo.bus)