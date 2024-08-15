from database.mysql_db_service import MySQLDatabase
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import validates, relationship

Base = MySQLDatabase.get_instance().base

class DemoUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    name = Column(String(40), nullable=False)
    email = Column(String(40 ), nullable=False, unique=True)
    licenses = relationship('DemoLicense')
    
    @validates('email')
    def validate_email(self, key, address):
        if not address:
            return

        if "@" not in address:
            raise ValueError("Not a valid email")
        return address

class DemoLicense(Base):
    __tablename__ = 'licenses'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, unique=True)
    license_number = Column(String(20), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey(DemoUser.id), nullable=False)
    is_active = Column(Boolean, default=True)

    user = relationship(DemoUser, back_populates='licenses')