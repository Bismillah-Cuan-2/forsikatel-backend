from flask import jsonify
from collections import defaultdict
from sqlalchemy import func, cast, Date
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from app.connections.db import Session
from app.models.data_model import Data
from app.models.users_model import Users
from app.models.hadist_kultum_model import HadistKultum
from app.constant.messages.error import Error
from app.constant.messages.dashboard import DashboardMessages

class DashboardServices:
    @staticmethod
    def get_last_juz(payload):
        with Session() as session:
            try:
                last_juz = session.query(Data.last_juz).filter(
                    Data.user_id == payload["user_id"],
                    Data.is_deleted == False
                ).order_by(Data.created_at.desc()).first()
                
                return last_juz[0] if last_juz else None  # Ambil hanya nilainya
            except Exception as e:
                session.rollback()
                return Error.messages(e)
            
    @staticmethod
    def kalender(payload):
        with Session() as session:
            try:
                result = (
                    session.query(func.date(Data.created_at))
                    .filter(
                        Data.user_id == payload["user_id"],
                        Data.is_deleted == False
                    )
                    .distinct()
                    .all()
                )

                hari_terisi = {datetime.strptime(str(row[0]), "%Y-%m-%d").isoweekday() for row in result}

                nama_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
                kalender = {nama_hari[i]: (i + 1 in hari_terisi) for i in range(7)}

                return kalender

            except Exception as e:
                session.rollback()
                return Error.messages(e)
            
    @staticmethod
    def hadits():
        with Session() as session:
            try:
                utc_now = datetime.now(ZoneInfo("UTC"))
                wib_now = utc_now.astimezone(ZoneInfo("Asia/Jakarta"))
                today = wib_now.day
                hadits = session.query(HadistKultum).filter(
                    HadistKultum.day == today, HadistKultum.is_deleted == False
                ).first()

                if hadits:
                    bagian_hadits = hadits.hadist.split("•", 1)  # Pisah berdasarkan "•" sekali
                    return {
                        "hadits": bagian_hadits[0].strip(),
                        "source": bagian_hadits[1].strip() if len(bagian_hadits) > 1 else ""
                    }

                return None
            except Exception as e:
                session.rollback()
                return Error.messages(e)
            
    @staticmethod
    def latest_activity():
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
                    .limit(5)
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
    def top_region():
        with Session() as session:
            try:
                region_totals = defaultdict(int)

                user_regions = session.query(Users.id, Users.regional).all()
                user_region_map = {user_id: region for user_id, region in user_regions}

                user_juz_totals = session.query(Data.user_id, func.sum(Data.juz_read)) \
                    .filter(Data.is_deleted == False) \
                    .group_by(Data.user_id) \
                    .all()

                for user_id, total_juz in user_juz_totals:
                    if user_id in user_region_map:
                        region_totals[user_region_map[user_id]] += total_juz

                top_regions = sorted(region_totals.items(), key=lambda x: x[1], reverse=True)[:3]

                return [{"region": region, "total_juz": total} for region, total in top_regions]
            except Exception as e:
                session.rollback()
                return Error.messages(e)
            
    @staticmethod
    def today_report_region():
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
    def time_in_day():
        try:
            utc_now = datetime.now(ZoneInfo("UTC"))
            wib_now = utc_now.astimezone(ZoneInfo("Asia/Jakarta"))
            hour = wib_now.hour

            if 4 <= hour < 10:
                return "Pagi"
            elif 10 <= hour < 15:
                return "Siang"
            elif 15 <= hour < 18:
                return "Sore"
            else:
                return "Malam"
        except Exception as e:
            return Error.messages(e)
        
    @staticmethod
    def get_name_husband(payload):
        with Session() as session:
            try:
                name_husband = session.query(Users.name_husband).filter_by(id=payload["user_id"]).first()
                
                if name_husband:
                    name_husband = name_husband[0]  # Ambil nilai dari tuple
                    
                    # Ambil hanya bagian sebelum tanda "-"
                    name_husband = name_husband.split("-")[0].strip()

                    # Ambil maksimal 2 kata pertama
                    words = name_husband.split()
                    name_husband = " ".join(words[:2])

                return name_husband
            except Exception as e:
                session.rollback()
                return Error.messages(e)
        
    @staticmethod
    def dashboard_data(payload):
        return jsonify({
            "last_juz": DashboardServices.get_last_juz(payload),
            "kalender": DashboardServices.kalender(payload),
            "hadits": DashboardServices.hadits(),
            "latest_activity": DashboardServices.latest_activity(),
            "top_region": DashboardServices.top_region(),
            "today_report_region": DashboardServices.today_report_region(),
            "time_in_day": DashboardServices.time_in_day(),
            "name_husband": DashboardServices.get_name_husband(payload),
            "message": DashboardMessages.SUCCESS_GET_DASHBOARD_DATA
        })
