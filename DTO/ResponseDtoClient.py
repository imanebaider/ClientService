from typing import Optional, List

class ResponseDtoClient:
    def __init__(self, id: int, cni: str, nom: str, prenom: str, email: str,
                 age: Optional[int] = None, photo_carte_identity: Optional[str] = None,
                 ):
        self.id = id
        self.cni = cni
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.age = age
        self.photo_carte_identity = photo_carte_identity
        #self.reservation_ids = reservation_ids or []  # relation avec les réservations

    def to_dict(self):
        return {
            "id": self.id,
            "cni": self.cni,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "age": self.age,
            "photo_carte_identity": self.photo_carte_identity,
            #"reservation_ids": self.reservation_ids,
        }
