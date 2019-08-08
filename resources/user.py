import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel



class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument(
		'username', type = str,
		required = True, 
		help = "User name field is mandatory")
	parser.add_argument(
		'password', type = str,
		required = True, 
		help = "Password field is mandatory")

	def post(self):
		data = UserRegister.parser.parse_args()
		
		if UserModel.find_by_username(data['username']):
			return {"message" : "user already exists"}, 400
		print("username : " + data['username'])
		print("password : " + data['password'])
		new_user = UserModel(data['username'],data['password'])
		print(new_user.username)
		print(new_user.password)
		new_user.save_to_db()

		return {"message" : "user has been created"}, 201