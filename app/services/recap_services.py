from flask import jsonify
from app.connections.db import Session
from sqlalchemy import func, cast, Date, exists, case
from datetime import datetime
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from app.models.data_model import Data
from app.models.users_model import Users
from app.constant.messages.error import Error
from app.constant.messages.recap import RecapMessages

class RecapServices:
    @staticmethod
    def total_khatam():
        try:
            with Session() as session:
                region_totals = defaultdict(int)

                # Ambil data user_id dan regional masing-masing
                user_regions = session.query(Users.id, Users.regional).all()
                user_region_map = {user_id: region for user_id, region in user_regions}

                # Subquery: Ambil created_at terbaru per user
                subquery = (
                    session.query(
                        Data.user_id,
                        func.max(Data.created_at).label("latest_created_at")
                    )
                    .filter(Data.is_deleted == False)
                    .group_by(Data.user_id)
                    .subquery()
                )

                # Ambil total_khatam hanya dari data terbaru per user berdasarkan created_at
                user_khatam_totals = (
                    session.query(
                        Data.user_id,
                        Data.total_khatam
                    )
                    .join(subquery, (Data.user_id == subquery.c.user_id) & (Data.created_at == subquery.c.latest_created_at))
                    .filter(Data.is_deleted == False)
                    .all()
                )

                # Akumulasi total juz berdasarkan region
                for user_id, total_khatam in user_khatam_totals:
                    if user_id in user_region_map:
                        region_totals[user_region_map[user_id]] += total_khatam or 0  # Hindari None

                # Mengembalikan semua region beserta total juz yang dihitung hanya dari data terbaru per user
                return [{"region": region, "total_khatam": total} for region, total in region_totals.items()]
        except Exception as e:
            session.rollback()
            return Error.messages(e)
        
    @staticmethod
    def total_juz():
        try:
            with Session() as session:
                region_totals = defaultdict(int)

                # Ambil data user_id dan region masing-masing
                user_regions = session.query(Users.id, Users.regional).all()
                user_region_map = {user_id: region for user_id, region in user_regions}

                # Ambil total juz yang telah dibaca per user
                user_juz_totals = session.query(
                        Data.user_id,
                        func.sum(Data.juz_read)
                    ) \
                    .filter(Data.is_deleted == False) \
                    .group_by(Data.user_id) \
                    .all()

                # Akumulasi total juz berdasarkan region
                for user_id, total_juz in user_juz_totals:
                    if user_id in user_region_map:
                        region_totals[user_region_map[user_id]] += total_juz

                # Mengembalikan semua region beserta total juz yang dibaca hari ini
                return [{"region": region, "total_juz": total} for region, total in region_totals.items()]
        except Exception as e:
            session.rollback()
            return Error.messages(e)
        
    @staticmethod
    def user_recap():
        try:
            today = datetime.now()

            with Session() as session:
                user_datas = session.query(
                    Data.user_id,
                    Users.name_husband,
                    Users.regional,
                    func.sum(Data.juz_read).label("total_juz")
                ) \
                .join(Users, Users.id == Data.user_id) \
                .filter(Data.is_deleted == False) \
                .group_by(Data.user_id, Users.name_husband, Users.regional) \
                .order_by(
                    case(
                        (Users.regional == 'ho', 0),
                        (Users.regional == 'r1_sumatera', 1),
                        (Users.regional == 'r2_jakarta', 2),
                        (Users.regional == 'r3_jabar', 3),
                        (Users.regional == 'r4_jateng_jogja', 4),
                        (Users.regional == 'r5_jatim_bali_nt', 5),
                        (Users.regional == 'r6_kalimantan', 6),
                        else_=7
                    )
                ) \
                .all()

                result = []
                for user_id, name_husband, regional, total_juz in user_datas:
                    latest_entry = session.query(Data.last_juz, Data.total_khatam) \
                        .filter(Data.user_id == user_id, Data.is_deleted == False) \
                        .order_by(Data.created_at.desc()) \
                        .first()

                    last_juz = latest_entry.last_juz if latest_entry else None
                    total_khatam = latest_entry.total_khatam if latest_entry else None

                    last_5days = []
                    for i in range(5, 0, -1):  # 5 hari lalu di kiri, terbaru di kanan
                        check_date = today - timedelta(days=i)
                        has_entry = session.query(Data.id) \
                            .filter(
                                Data.user_id == user_id,
                                func.date(Data.created_at) == check_date.date(),
                                Data.is_deleted == False
                            ).first()
                        last_5days.append(bool(has_entry))

                    result.append({
                        "user_id": user_id,
                        "name_husband": name_husband,
                        "regional": regional,
                        "total_juz": total_juz,
                        "last_juz": last_juz,
                        "total_khatam": total_khatam,
                        "last_5days": last_5days
                    })

                return result

        except Exception as e:
            session.rollback()
            return Error.messages(e)
        
    @staticmethod
    def recap_data():
        return jsonify({
            "total_khatam_region": RecapServices.total_khatam(),
            "total_juz_region": RecapServices.total_juz(),
            "detail_person": RecapServices.user_recap()
        })
        
        