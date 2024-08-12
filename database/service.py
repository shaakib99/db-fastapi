from database.lib.db_abc import DatabaseABC
from database.mysql_db_service import MySQLDatabase
from typing import Generic, TypeVar

T = TypeVar("T")

class DatabaseService(Generic[T]):
    def __init__(self, schema, Service: DatabaseABC = MySQLDatabase):
        self.service = Service.get_instance()
        self.schema = schema
    
    def connect(self):
        self.service.connect()
    
    def disconnect(self):
        self.service.disconnect()
    
    def create_metadata(self):
        self.service.create_metadata()
    
    def getOne(self, id: str) -> T:
        return self.service.getOneById(self.schema, id)

    def getAll(self, query) -> list[T]:
        return self.service.getAll(self.schema, query)
    
    def saveOne(self, data: dict) -> T:
        return self.service.saveOne(self.schema, data)
    
    def updateOne(self, id: str, data: dict) -> T:
        return self.service.updateOne(self.schema, id, data)
    
    def deleteOne(self, id: str) -> None:
        return self.service.deleteOne(self.schema, id)