from sqlalchemy import Column, Integer, String
from entity.base import Base

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cni = Column(String(50), nullable=False)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    photo_carte_identity = Column(String(255), nullable=True)
