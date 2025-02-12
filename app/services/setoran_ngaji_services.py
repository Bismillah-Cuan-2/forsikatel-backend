from flask import jsonify
from app.connections.db import Session
from datetime import datetime, timedelta, timezone
from app.models.data_model import Data
from app.constant.messages.error import Error
from zoneinfo import ZoneInfo
from sqlalchemy import func
from app.constant.messages.setoran_ngaji import SetoranNgajiMessages

class Dataservices:
    @staticmethod
    def add_setoran(user_id, juz_read):
        with Session() as session:
            try:
                if not user_id or not juz_read:
                    return jsonify({"msg": SetoranNgajiMessages.MISSING_DATA}), 400

                total_juz_sebelumnya = session.query(func.sum(Data.juz_read)).filter(
                    Data.user_id == user_id, Data.is_deleted == False
                ).scalar() or 0

                total_juz_baru = total_juz_sebelumnya + juz_read
                total_khatam = total_juz_baru // 30  
                last_juz = (total_juz_baru % 30) if (total_juz_baru % 30) != 0 else 30

                setoran = Data(
                    user_id=user_id,
                    juz_read=juz_read,
                    last_juz=last_juz,
                    total_khatam=total_khatam
                )

                session.add(setoran)
                session.commit()
                
                return jsonify({"msg": SetoranNgajiMessages.SUCCESS_ADD_SETOR_NGAJI_DATA,
                                "new_setoran": setoran.to_dict()}), 201
            
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400

    @staticmethod
    @staticmethod
    def all_storage(user_id):
        with Session() as session:
            try:
                setoran_list = session.query(Data).filter(
                    Data.user_id == user_id, Data.is_deleted == False
                ).order_by(Data.created_at.desc()).all()

                if not setoran_list:
                    return jsonify({"msg": SetoranNgajiMessages.SETORAN_NOT_FOUND}), 404

                result = []
                for setoran in setoran_list:
                    result.append({
                        "tanggal": setoran.created_at.strftime("%d %b %Y"),
                        "banyak_juz_dibaca": setoran.juz_read,
                        "juz_terakhir": setoran.last_juz,
                        "total_khatam": f"{setoran.total_khatam}x"
                    })

                total_juz = session.query(func.sum(Data.juz_read)).filter(
                    Data.user_id == user_id, Data.is_deleted == False
                ).scalar() or 0

                total_khatam = total_juz // 30  

                last_juz = session.query(Data.last_juz).filter(
                    Data.user_id == user_id, Data.is_deleted == False
                ).order_by(Data.created_at.desc()).first()

                
                today = datetime.today()
                last_week = today - timedelta(days=7)
                prev_week_start = last_week - timedelta(days=7)

                recent_data = session.query(
                    func.date(Data.created_at), func.sum(Data.juz_read)
                ).filter(
                    Data.user_id == user_id,
                    Data.created_at >= last_week,
                    Data.is_deleted == False
                ).group_by(func.date(Data.created_at)).all()

                prev_data = session.query(
                    func.date(Data.created_at), func.sum(Data.juz_read)
                ).filter(
                    Data.user_id == user_id,
                    Data.created_at >= prev_week_start,
                    Data.created_at < last_week,
                    Data.is_deleted == False
                ).group_by(func.date(Data.created_at)).all()

                return jsonify({
                    "msg": SetoranNgajiMessages.SUCCESS_ADD_STORAGE,
                    "history": result,
                    "total_progress": {
                        "total_juz": total_juz,
                        "last_juz": last_juz[0] if last_juz else 0,
                        "total_khatam": total_khatam
                    },
                    "progress_chart": {
                        "msg": SetoranNgajiMessages.SUCCESS_PROGRESS_CHART,
                        "data": {
                            "last_7_days": {str(date): juz for date, juz in recent_data},
                            "prev_week": {str(date): juz for date, juz in prev_data}
                        }
                    }
                }), 200

            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
