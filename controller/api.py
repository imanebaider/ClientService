from flask_restx import Namespace, Resource, fields
from flask import request
from service.ClientService import ClientService
from Repository.ClientRepository import ClientRepository
from DTO.RequestDtoClient import RequestDtoClient
from Mapper.ClientMapper import dto_to_entity, entity_to_dto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entity.Client import Client
 # <--- Import de ton entity Client

# ----------------- Config DB -----------------
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/gestion_client"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db_session = SessionLocal()

# ----------------- Repository & Service -----------------
repository = ClientRepository(db_session)
client_service = ClientService(repository)

# ----------------- Namespace -----------------
ns = Namespace('clients', description='Opérations sur les clients')

client_model = ns.model('Client', {
    'id': fields.Integer(readOnly=True),
    'cni': fields.String(required=True),
    'nom': fields.String(required=True),
    'prenom': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'age': fields.Integer(),
    'photo_carte_identity': fields.String(),
    'reservation_ids': fields.List(fields.Integer)
})

# ----------------- Routes -----------------
@ns.route('/')
class ClientList(Resource):
    @ns.marshal_list_with(client_model)
    def get(self):
        """Lister tous les clients"""
        # Query tous les clients depuis la DB
        clients_entities = db_session.query(Client).all()
        # Convertir en DTO puis en dict pour la réponse
        clients = [entity_to_dto(c).to_dict() for c in clients_entities]
        return clients

    @ns.expect(client_model)
    @ns.marshal_with(client_model, code=201)
    def post(self):
        """Ajouter un client"""
        data = request.json
        dto = RequestDtoClient(**data)
        client = client_service.add_client(dto)
        return client.to_dict(), 201

@ns.route('/<int:id>')
class ClientResource(Resource):
    @ns.marshal_with(client_model)
    def get(self, id):
        """Récupérer un client par ID"""
        client = client_service.get_client(id)
        if client:
            return client.to_dict()
        ns.abort(404, "Client non trouvé")

    @ns.expect(client_model)
    @ns.marshal_with(client_model)
    def put(self, id):
        """Mettre à jour un client"""
        data = request.json
        updated_client = client_service.update_client(id, data)
        if updated_client:
            return updated_client.to_dict()
        ns.abort(404, "Client non trouvé")

    def delete(self, id):
        """Supprimer un client par ID"""
        success = client_service.delete_client(id)
        if success:
            return {"message": f"Client avec id {id} supprimé"}, 200
        ns.abort(404, "Client non trouvé")

