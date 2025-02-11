from app.connections.db import engine, Base
from app.models.users_model import Users

# Membuat semua tabel yang belum ada berdasarkan model
Base.metadata.create_all(engine)

print("Success update database")