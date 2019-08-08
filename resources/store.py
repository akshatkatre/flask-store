from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        
        return {'message' : 'Store not found'}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message' : 'Store already exists'}, 400
        store = StoreModel(name)
        store.save_to_db()
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {'message' : 'error occured'}, 500
        
        return {'message' : 'store {} has been deleted'.format(name)}


class StoreList(Resource):
    def get(self):
        return {'stores' : list(map(lambda x:x.json(), StoreModel.query.all() ))}