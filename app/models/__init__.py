from app.connections.db import engine, Base
from app.models.hadist_kultum_model import HadistKultum

# Membuat semua tabel yang belum ada berdasarkan model
Base.metadata.create_all(engine)

print("Success update database")