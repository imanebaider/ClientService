from sqlalchemy.orm import Session
from entity.Client import Client

class ClientRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    # ----------------- CRUD -----------------
    def save(self, client: Client):
        """إضافة عميل جديد أو تحديث موجود"""
        self.db_session.add(client)
        self.db_session.commit()
        return client

    def find_by_id(self, id: int):
        """جلب عميل حسب id"""
        return self.db_session.query(Client).filter_by(id=id).first()

    def update(self, id: int, client_data: dict):
        """تحديث بيانات العميل حسب id"""
        client = self.find_by_id(id)
        if client:
            for key, value in client_data.items():
                setattr(client, key, value)
            self.db_session.commit()
        return client

    def delete(self, id: int):
        """حذف العميل حسب id"""
        client = self.find_by_id(id)
        if client:
            self.db_session.delete(client)
            self.db_session.commit()
        return client
