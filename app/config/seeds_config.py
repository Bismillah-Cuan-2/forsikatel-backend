from app.models.users_model import Users
from app.seeds.user_seeds import user_seeds
from app.models.data_model import Data
from app.seeds.setoran_seeds import setoran_seed
seed_configs = {
        "users": {
            "model": Users,
            "data": user_seeds,
            "fields": ["name_husband", "regional", "phone_number"],
            "process_function": lambda session, user_seeds: (
                lambda user: (user.set_phone_number(user_seeds["phone_number"]), user)[1])
                (Users(name_husband=user_seeds["name_husband"], regional=user_seeds["regional"]))
        },
        "setoran": {
            "model": Data,
            "data": setoran_seed,
            "fields": ["user_id", "juz_read", "last_juz", "total_khatam"],
            "process_function": lambda session, setoran_seed:Data(
                user_id = setoran_seed["user_id"],    
                juz_read = setoran_seed["juz_read"],
                last_juz = setoran_seed["last_juz"],
                total_khatam = setoran_seed["total_khatam"],
            ) 
        }
    }