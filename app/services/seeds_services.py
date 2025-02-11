from flask import jsonify
from app.connections.db import Session
from app.config.seeds_config import seed_configs
from app.constant.messages.seeds import SeedMessages
from app.constant.messages.error import Error
from sqlalchemy import text
from app.constant.SQL import Query
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeedsService:
    @staticmethod
    def generate_all_seed(data):
        seeds = data["seeds_type"]

        if seeds not in seed_configs:
            return jsonify({
                "msg": SeedMessages.INVALID_SEEDS_TYPE
            }), 400

        seed_config = seed_configs[seeds]
        model = seed_config["model"]
        data_list = seed_config["data"]
        process_function = seed_config["process_function"]

        with Session() as session:
            try:
                logger.info(f"Seeding data for: {seeds}")

                # Check if data already exists
                if session.query(model).count() != 0:
                    return jsonify({
                        "msg": SeedMessages.SEEDS_ALREADY_EXIST
                    }), 400

                # Generate seed data
                new_objects = [process_function(session, item) for item in data_list]

                # Save to database
                session.add_all(new_objects)
                session.commit()

                return jsonify({
                    "msg": SeedMessages.SUCCESS_ADD_SEEDS_DATA
                }), 201

            except Exception as e:
                session.rollback()
                logger.error(f"Error during seeding: {e}")
                return jsonify(Error.messages(e)), 400
        
    @staticmethod
    def show_seeds(data):
        seeds = data["seeds_type"]

        if seeds not in seed_configs:
            return jsonify({
                "msg": SeedMessages.INVALID_SEEDS_TYPE
            }), 400

        seed_config = seed_configs[seeds]
        model = seed_config["model"]

        with Session() as session:
            try:
                logger.info(f"Fetching seed data for: {seeds}")

                # Fetch all records for the specified seed type
                records = session.query(model).all()
                record_list = [record.to_dict() for record in records]

                return jsonify({
                    "msg": SeedMessages.SUCCESS_SHOW_ALL_SEED,
                    seeds: record_list
                }), 200

            except Exception as e:
                logger.error(f"Error while fetching seeds: {e}")
                session.rollback()
                return jsonify(Error.messages(e)), 400

    @staticmethod
    def clear_seeds(data):
        seeds = data["seeds_type"]

        if seeds not in seed_configs:
            return jsonify({
                "msg": SeedMessages.INVALID_SEEDS_TYPE
            }), 400

        seed_config = seed_configs[seeds]
        model = seed_config["model"]

        with Session() as session:
            try:
                logger.info(f"Clearing seed data for: {seeds}")

                # Delete all records for the specified seed type
                session.query(model).delete()
                session.execute(text(Query.reset_primary_key(model.__tablename__)))

                session.commit()

                return jsonify({
                    "msg": SeedMessages.CLEAR_SEEDS_DATA
                }), 200

            except Exception as e:
                logger.error(f"Error while clearing seeds: {e}")
                session.rollback()
                return jsonify(Error.messages(e)), 400