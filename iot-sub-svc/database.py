from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
from models import Base, MQTTMessage
import logging
from config import Config

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_url: str = None):
        self.cfg = Config()
        self.db_url = db_url or self.cfg.db_url
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
    def _check_tables_exist(self) -> bool:
        inspector = inspect(self.engine)
        return 'mqtt_messages' in inspector.get_table_names()
    
    def init_db(self):
        if not self._check_tables_exist():
            try:
                Base.metadata.create_all(self.engine)
                logger.info("Database tables created successfully")
            except SQLAlchemyError as e:
                logger.error(f"Failed to create database tables: {str(e)}")
                raise
        else:
            logger.debug("Database tables already exist")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    # 在现有基础上增加操作异常处理
    def save_message(self, message):
        try:
            self.session.add(message)
            self.session.commit()
            logger.debug(f"Message saved, ID: {message.id}")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Failed to save message: {str(e)}")
            logger.debug(f"Failed message content: {message}")
            raise
