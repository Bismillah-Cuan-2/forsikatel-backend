from app.connections.db import engine, Base
from app.models.users_model import Users
from app.models.hadist_kultum_model import HadistKultum
from app.models.data_model import Data

# Membuat semua tabel yang belum ada berdasarkan model
Base.metadata.create_all(engine)

print("Success update database")