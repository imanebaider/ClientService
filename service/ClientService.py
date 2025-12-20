from Repository import ClientRepository
from DTO import RequestDtoClient
from Mapper.ClientMapper import dto_to_entity, entity_to_dto

class ClientService:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def add_client(self, dto: RequestDtoClient):
        """إضافة عميل جديد"""
        client = dto_to_entity(dto)
        self.repository.save(client)
        return entity_to_dto(client)

    def get_client(self, id: int):
        """جلب عميل حسب id"""
        client = self.repository.find_by_id(id)
        return entity_to_dto(client) if client else None

    def update_client(self, id: int, data: dict):
        """تحديث بيانات العميل حسب id"""
        client = self.repository.find_by_id(id)  # <-- correction hna
        if not client:
            return None
        for key, value in data.items():
            setattr(client, key, value)
        self.repository.save(client)  # ou update si t7eb t3ayet update
        return entity_to_dto(client)
    
    # f service/ClientService.py

    def delete_client(self, id: int):
        client = self.repository.find_by_id(id)
        if not client:
            return False
        self.repository.delete(id)
        return True

