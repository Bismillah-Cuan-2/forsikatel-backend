from app.models.users_model import Users
from app.seeds.user_seeds import user_seeds

seed_configs = {
        "users": {
            "model": Users,
            "data": user_seeds,
            "fields": ["name_husband", "regional", "phone_number"],
            "process_function": lambda session, user_seeds: (
                lambda user: (user.set_phone_number(user_seeds["phone_number"]), user)[1])
                (Users(name_husband=user_seeds["name_husband"], regional=user_seeds["regional"]))
        }
    }