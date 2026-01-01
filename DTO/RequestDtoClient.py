from typing import Optional, List

class RequestDtoClient:
    def __init__(self, cni: str, nom: str, prenom: str, email: str, password: str,
                 age: Optional[int] = None, photo_carte_identity: Optional[str] = None,
                 reservation_ids: Optional[List[int]] = None):
        self.cni = cni
        self.nom = nom
        self.prenom = prenom
        #self.email = email
        self.age = age
        self.photo_carte_identity = photo_carte_identity
        self.reservation_ids = reservation_ids or []  # relation avec les réservations

    @staticmethod
    def from_dict(data: dict):
        return RequestDtoClient(
            cni=data.get("cni"),
            nom=data.get("nom"),
            prenom=data.get("prenom"),
            #email=data.get("email"),
            age=data.get("age"),
            photo_carte_identity=data.get("photo_carte_identity"),
            reservation_ids=data.get("reservation_ids", []),
        )
