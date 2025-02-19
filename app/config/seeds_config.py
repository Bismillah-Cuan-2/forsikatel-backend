from app.models.users_model import Users
from app.seeds.user_seeds import user_seeds
from app.models.data_model import Data
from app.seeds.setoran_seeds import setoran_seed
from app.models.hadist_kultum_model import HadistKultum
from app.seeds.hadist_seeds import hadist_seeds
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
        },
        "hadist": {
            "model": HadistKultum,
            "data": hadist_seeds,
            "fields": ["hadist", "kultum", "day", "title", "channel"],
            "process_function": lambda session, hadist_seeds:HadistKultum(
                hadist = hadist_seeds["hadist"],
                kultum = hadist_seeds["kultum"],
                day = hadist_seeds["day"],
                title = hadist_seeds["title"],
                channel = hadist_seeds["channel"]
            ) 
        },
    }