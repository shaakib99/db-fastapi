from database.lib.db_abc import DatabaseABC
from database.models.query_param_model import SQLQueryParam
from sqlalchemy import create_engine,text, select
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import os

class MySQLDatabase(DatabaseABC):
    instance = None
    def __init__(self):
        self.engine = create_engine(os.getenv("DB_CONNECTION_URL", "mysql://test"))
        self.session: Session = sessionmaker(bind=self.engine, autoflush=False, autocommit = False)()
        self.base = declarative_base()
        self.base.metadata.create_all()

    def connect(self):
        self.engine.connect()

    def disconnect(self):
        self.engine.dispose(close=True)

    def get_instance() -> "DatabaseABC":
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
        if query.where:
            cursor = cursor.where(text(query.where))
        if query.group_by:
            cursor = cursor.group_by(text(query.group_by))
        if query.having:
            cursor = cursor.having(text(query.having))
        if query.order_by:
            cursor = cursor.order_by(text(query.order_by))

        cursor = cursor.limit(query.limit)
        cursor = cursor.offset(query.skip)

        return cursor.all()

    def saveOne(self, schema: DeclarativeBase, data: BaseModel):
        data = schema(**BaseModel)
        self.session.add(data)
        self.session.commit()
        self.session.flush()
        return data

    def deleteOne(self, schema, id: str):
        return self.session.delete(schema(id = id))