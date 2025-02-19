from flask import jsonify
from app.connections.db import Session
from sqlalchemy import func, cast, Date
from datetime import datetime
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from app.models.data_model import Data
from app.models.users_model import Users
from app.constant.messages.error import Error
from app.constant.messages.progress import ProgressMessages

class ProgressServices:
    @staticmethod
    def total_juz_region():
        today = datetime.now(timezone.utc).date()
        try:
            with Session() as session:
                region_totals = defaultdict(int)

                # Ambil data user_id dan region masing-masing
                user_regions = session.query(Users.id, Users.regional).all()
                user_region_map = {user_id: region for user_id, region in user_regions}

                # Ambil total juz yang telah dibaca per user **hanya untuk hari ini**
                user_juz_totals = session.query(
                        Data.user_id,
                        func.sum(Data.juz_read)
                    ) \
                    .filter(Data.is_deleted == False, cast(Data.created_at, Date) == today) \
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
    def total_setoran_region():
        try:
            today = datetime.now(timezone.utc).date()
            with Session() as session:
                result = (
                    session.query(
                        Users.regional, func.count(func.distinct(Data.user_id)).label("total_users_setor")
                    )
                    .join(Users, Users.id == Data.user_id)
                    .filter(cast(Data.created_at, Date) == today)
                    .group_by(Users.regional)
                    .all()
                )
                
                # Hitung total pengguna per region
                total_users_per_region = dict(
                    session.query(Users.regional, func.count(Users.id)).group_by(Users.regional).all()
                )
            return [{"region": region, "total_users_setor": total, "total_users_region": total_users_per_region.get(region, 0)} for region, total in result]
        except Exception as e:
            session.rollback()
            return Error.messages(e)
        
    @staticmethod
    def all_latest_activity():
        with Session() as session:
            try:
                latest_activities = (
                    session.query(
                        Data.created_at,
                        Users.name_husband,
                        Users.regional,
                        Data.last_juz,
                        Data.juz_read
                    )
                    .join(Users, Users.id == Data.user_id)
                    .filter(Data.is_deleted == False)
                    .order_by(Data.created_at.desc())
                    .all()
                )

                result = []
                for activity in latest_activities:
                    created_at, name, regional, last_juz, juz_read = activity
                    
                    # Hitung juz yang dibaca
                    start_juz = max(1, last_juz - juz_read + 1)  # Pastikan tidak kurang dari 1
                    end_juz = last_juz
                    juz_range = f"Juz {start_juz}-{end_juz}" if start_juz != end_juz else f"Juz {start_juz}"
                    
                    result.append({
                        "region": regional,
                        "name": name,
                        "juz_read": juz_range,
                        "entry_time": created_at.isoformat()
                    })
                
                return result
            except Exception as e:
                session.rollback()
                return Error.messages(e)
            
    @staticmethod
    def progress_data():
        return jsonify({
            "all_latest_activity": ProgressServices.all_latest_activity(),
            "total_setoran_region": ProgressServices.total_setoran_region(),
            "total_juz_region": ProgressServices.total_juz_region(),
            "message": ProgressMessages.SUCCESS_GET_PROGRESS_DATA
        })