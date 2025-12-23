from flask import Flask, request
from flask_restx import Namespace, Resource, fields, Api
from service.ClientService import ClientService
from Repository.ClientRepository import ClientRepository
from DTO.RequestDtoClient import RequestDtoClient
from Mapper.ClientMapper import dto_to_entity, entity_to_dto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entity.Client import Client
from config.security import require_role

# ----------------- App & DB Config -----------------
app = Flask(__name__)

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/gestion_client"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db_session = SessionLocal()

repository = ClientRepository(db_session)
client_service = ClientService(repository)

# ----------------- Swagger JWT Security -----------------
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "JWT Token. Format: 'Bearer <token>'"
    }
}

api = Api(
    app,
    version="1.0",
    title="Client API",
    description="API gestion des clients",
    authorizations=authorizations,
    security='Bearer Auth'  # default security for Swagger
)

# ----------------- Namespace -----------------
ns = Namespace('clients', description='Opérations sur les clients')
api.add_namespace(ns, path='/clients')

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

    @require_role("ADMIN")
    @ns.marshal_list_with(client_model)
    @ns.doc(security='Bearer Auth')
    def get(self):
        """Lister tous les clients (ADMIN uniquement)"""
        clients_entities = db_session.query(Client).all()
        clients = [entity_to_dto(c).to_dict() for c in clients_entities]
        return clients

    @ns.expect(client_model)
    @ns.marshal_with(client_model, code=201)
    @ns.doc(security=[])
    def post(self):
        """Ajouter un client (any visitor peut créer un compte)"""
        data = request.json
        dto = RequestDtoClient(**data)
        client = client_service.add_client(dto)
        return client.to_dict(), 201

@ns.route('/<int:id>')
class ClientResource(Resource):

    @require_role("CLIENT", "ADMIN")
    @ns.marshal_with(client_model)
    @ns.doc(security='Bearer Auth')
    def get(self, id):
        """Récupérer un client par ID (CLIENT ou ADMIN)"""
        client = client_service.get_client(id)
        if client:
            return client.to_dict()
        ns.abort(404, "Client non trouvé")

    @require_role("CLIENT", "ADMIN")
    @ns.expect(client_model)
    @ns.marshal_with(client_model)
    @ns.doc(security='Bearer Auth')
    def put(self, id):
        """Mettre à jour un client (CLIENT ou ADMIN)"""
        data = request.json
        updated_client = client_service.update_client(id, data)
        if updated_client:
            return updated_client.to_dict()
        ns.abort(404, "Client non trouvé")

    @require_role("CLIENT", "ADMIN")
    @ns.doc(security='Bearer Auth')
    def delete(self, id):
        """Supprimer un client par ID (CLIENT ou ADMIN)"""
        success = client_service.delete_client(id)
        if success:
            return {"message": f"Client avec id {id} supprimé"}, 200
        ns.abort(404, "Client non trouvé")

# ----------------- Main -----------------
if __name__ == "__main__":
    app.run(debug=True, port=8088)
