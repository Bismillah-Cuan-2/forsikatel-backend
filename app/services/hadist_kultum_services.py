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
                today = datetime.now(timezone.utc).day
                hadist_kultum = session.query(HadistKultum).filter(
                    HadistKultum.day == today, HadistKultum.is_deleted == False).first()
                
                return jsonify({
                    "message": HadistKultumMessages.SUCCESS_GET_HADIST_KULTUM,
                    "hadist_kultum": hadist_kultum.to_dict() if hadist_kultum else {}
                })
            except Exception as e:
                return jsonify(Error.messages(e)), 500
    
    def load_hadist_kultum_from_excel(file_path):
        with Session() as session:
            try:
                df = pd.read_excel(file_path)

                required_columns = {"hadist", "kultum", "day"}
                if not required_columns.issubset(df.columns):
                    return jsonify({"error": "Missing required columns in Excel"}), 400

                for _, row in df.iterrows():
                    # Pastikan nilai "day" adalah angka antara 1-31
                    if not (1 <= int(row["day"]) <= 31):
                        continue  # Skip jika day tidak valid

                    new_hadist_kultum = HadistKultum(
                        hadist=row["hadist"],
                        kultum=row["kultum"],
                        day=int(row["day"])
                    )
                    session.add(new_hadist_kultum)

                session.commit()
                return jsonify({"message": HadistKultumMessages.SUCCESS_LOAD_HADIST_KULTUM}), 201

            except Exception as e:
                session.rollback()
                return jsonify(Error.messages(e)), 400