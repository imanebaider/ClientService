from entity.Client import Client
from DTO.RequestDtoClient import RequestDtoClient
from DTO.ResponseDtoClient import ResponseDtoClient

def dto_to_entity(dto: RequestDtoClient) -> Client:
    return Client(
        cni=dto.cni,
        nom=dto.nom,
        prenom=dto.prenom,
        #email=dto.email,
        age=dto.age,
        photo_carte_identity=dto.photo_carte_identity
    )

def entity_to_dto(entity: Client) -> ResponseDtoClient:
    return ResponseDtoClient(
        id=entity.id,
        cni=entity.cni,
        nom=entity.nom,
        prenom=entity.prenom,
        email=entity.email,
        age=entity.age,
        photo_carte_identity=entity.photo_carte_identity
    )
