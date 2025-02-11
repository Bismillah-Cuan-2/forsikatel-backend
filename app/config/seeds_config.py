from app.models.users_model import Users
from app.seeds.user_seeds import user_seeds

seed_configs = {
    "users": {
        "model": Users,
        "data": user_seeds,
        "fields": ["name_husband", "regional", "phone_number"],
        "process_function": lambda session, user_seed: Users(
            name_husband=user_seed["name_husband"],
            regional=user_seed["regional"]
        ).set_phone_number(user_seed["phone_number"])
    }
}
