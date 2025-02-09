from app.connections.db import engine, Base

# Membuat semua tabel yang belum ada berdasarkan model
Base.metadata.create_all(engine)

print("Success update database")