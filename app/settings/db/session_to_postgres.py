from app.settings import config_settings
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker


def create_dbsession(**kwargs):
    db_path = config_settings.db_url
    engine = db.create_engine(db_path)
    SessionClass = sessionmaker(bind=engine)
    return SessionClass()
