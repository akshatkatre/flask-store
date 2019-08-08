import sqlite3
from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument(
		'price', type = float,
		required = True, 
		help = "This field is mandatory")
	parser.add_argument(
		'store_id', type = int,
		required = True, 
		help = "Every item needs to store id")

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		else:
			return {'message' : 'item not found in database'}, 404

	def post(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return {"message" : "Item {} already exists".format(name)}, 400
		data = Item.parser.parse_args()	
		item = ItemModel(name, **data)
		try:
			item.save_to_db()
		except:
			return {'message' : 'An error occured when inserting the item.'}, 500

		return item.json(), 201

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		
		return {"message" : "Item deleted"}

	def put(self, name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)
		if item is None:
			item = ItemModel(name, data['price'], data['store_id'])
		else:
			item.price = data['price']
			item.store_id = data['store_id']
		
		item.save_to_db()
		return item.json()


class Items(Resource):
	def get(self):
		#List comprehensions
		#return {'items' : [item.json() for item in ItemModel.query.all()]}
		#Lambda expressions
		return {'items' : list(map(lambda x: x.json(), ItemModel.query.all()))}