from abc import abstractmethod, ABC

class DatabaseABC(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def create_metadata(self):
        pass

    @staticmethod
    @abstractmethod
    def get_instance() -> "DatabaseABC":
        pass

    @abstractmethod
    def getOneById(self, schema, id: str):
        pass

    @abstractmethod
    def getAll(self, schema, query):
        pass

    @abstractmethod
    def saveOne(self, schema, data: dict):
        pass

    @abstractmethod
    def updateOne(self, schema, id: str, data: dict):
        pass

    @abstractmethod
    def deleteOne(self, schema, id: str):
        pass