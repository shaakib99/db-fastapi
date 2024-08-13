from database.lib.db_abc import DatabaseABC
from database.models.query_param_model import SQLQueryParam
from sqlalchemy import create_engine,text, select
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
import os

class MySQLDatabase(DatabaseABC):
    instance = None
    def __init__(self):
        self.engine = create_engine(os.getenv('DB_CONNECTION_URL', 'mysql://test'))
        self.session: Session = sessionmaker(bind=self.engine, autoflush=False, autocommit = False)()
        self.base = declarative_base()
        self.base.metadata.create_all(self.engine)

    def connect(self):
        self.engine.connect()

    def disconnect(self):
        self.engine.dispose(close=True)
    
    def create_metadata(self):
        self.base.metadata.create_all(self.engine)

    def get_instance() -> 'MySQLDatabase':
        if MySQLDatabase.instance is None:
            MySQLDatabase.instance = MySQLDatabase()
        return MySQLDatabase.instance


    def getOneById(self, schema: DeclarativeBase, id: str):
        cursor = self.session.query(schema)
        return cursor.get(id)
        

    def getAll(self, schema: DeclarativeBase, query: SQLQueryParam):
        cursor = self.session.query(schema)
        
        if query.selected_fields:
            cursor = cursor.add_columns(select(query.selected_fields))
        if query.filter_by:
            cursor = cursor.where(text(query.filter_by))
        if query.group_by:
            cursor = cursor.group_by(text(query.group_by))
        if query.having:
            cursor = cursor.having(text(query.having))
        if query.order_by:
            cursor = cursor.order_by(text(query.order_by))

        cursor = cursor.limit(query.limit)
        cursor = cursor.offset(query.skip)

        return cursor.all()

    def saveOne(self, schema: DeclarativeBase, data: dict):
        try:
            data_model = schema(**data)
            self.session.add(data_model)
            self.session.commit()
            return data_model
        except Exception as e:
            self.session.rollback()
            self.session.reset()
            raise Exception(str(e))
    
    def updateOne(self, schema: DeclarativeBase, id: str, data: dict):
        try:
            data_model = schema(**data)
            self.session.commit()
            return data_model
        except Exception as e:
            self.session.rollback()
            self.session.reset()
            raise Exception(str(e))

    def deleteOne(self, schema: DeclarativeBase, id: str):
        try:
            return self.session.delete(schema(id = id))
        except Exception as e:
            self.session.rollback()
            self.session.reset()
            raise Exception(str(e))