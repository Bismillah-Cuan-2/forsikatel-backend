from flask import jsonify
from app.connections.db import Session
from datetime import datetime, timedelta, timezone
from app.models.hadist_kultum_model import HadistKultum
from app.constant.messages.error import Error
from app.constant.messages.hadist_kultum import HadistKultumMessages
import pandas as pd

class HadistKultumServices:
    @staticmethod
    def get_daily_hadist():
        with Session() as session:
            try:
                today = datetime.now(timezone.utc).date()
                hadist_kultum = session.query(HadistKultum).filter(
                    HadistKultum.display_date == today, HadistKultum.is_deleted == False).first()

                if not hadist_kultum:
                    HadistKultumServices.update_daily_hadist_kultum()
                    hadist_kultum = session.query(HadistKultum).filter(
                        HadistKultum.display_date == today, HadistKultum.is_deleted == False).first()
                
                return jsonify({
                    "message": "...",
                    "hadist_kultum": hadist_kultum.to_dict() if hadist_kultum else {}
                })
            except Exception as e:
                return jsonify(Error.messages(e)), 500
    
    @staticmethod
    def update_daily_hadist_kultum():
        with Session() as session:
            try:
                today = datetime.now(timezone.utc).date()
                update_hadist_kultum = session.query(HadistKultum).filter(
                    HadistKultum.display_date == None, HadistKultum.is_deleted == False).order_by(HadistKultum.id).first()
                
                if not update_hadist_kultum:
                    HadistKultumServices.reset_hadist_kultum_display()
                    update_hadist_kultum = session.query(HadistKultum).filter(
                        HadistKultum.display_date == None,
                        HadistKultum.is_deleted == False
                    ).order_by(HadistKultum.id).first()
                
                if update_hadist_kultum:
                    update_hadist_kultum.display_date = today
                    session.add(update_hadist_kultum)
                    session.commit()
                    return jsonify({
                        "message": HadistKultumMessages.SUCCESS_RESET_HADIST_KULTUM
                    })
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400
    #kemungkinan dihapus
    def initialize_hadist_kultum_():
        HadistKultumServices.scheduler.add_job(
            HadistKultumServices.update_daily_hadist_kultum,
            'interval',
            days=1,
            run_time=datetime.now() + timedelta(seconds=5) #caritau formatnya
        )
        HadistKultumServices.scheduler.start()
    
    def load_hadist_kultum_from_excel(file_path):
        with Session() as session:
            try:
                df = pd.read_excel(file_path)
                for _, row in df.iterrows():
                    new_hadist_kultum = HadistKultum(
                        hadist=row["hadist"],
                        kultum=row["kultum"] #tambah kolom tanggal aja gausah bulan tahun nya (display date)
                    )
                    session.add(new_hadist_kultum)
                
                session.commit()
                return jsonify({"message": "..."}), 201
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400

    def reset_hadist_kultum_display():
        with Session() as session:
            try:
                hadist_kultum = session.query(HadistKultum).filter(
                    HadistKultum.display_date == None, HadistKultum.is_deleted == False).order_by(HadistKultum.id).first()
                
                if hadist_kultum:
                    hadist_kultum.display_date = datetime.now(timezone.utc).date()
                    session.add(hadist_kultum)
                    session.commit()
                    return jsonify({
                        "message": HadistKultumMessages.SUCCESS_RESET_HADIST_KULTUM
                    })
            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400