from flask import Response
import json, pymongo
from bson.objectid import ObjectId

""" How to Use This Module
	@create
		tabel = db.pengguna //just example collection name
		data = {"userName" : "bakpionalx","firstName" : "qre"}
		crud.create(tabel,data)
	@read
		All data
			tabel = db.pengguna //just example collection name
			crud.read(tabel)
		All Spesific Data
			tabel = db.pengguna //just example collection name
			parameter = {"userName" : "bakpionalx"}
			crud.read(tabel,parameter)
	@update
		tabel = db.pengguna
		parameter = {"userName": "example"} //index of
		data = {"firstName" : "teong", "lastname" : "exampleage"} //parameter
		crud.update(tabel,index,parameter)
	@delete
		tabel = db.pengguna
		parameter = {"userName": "example"}
		crud.delete(tabel,parameter)
"""

def mongo2Json(documents):
	response = []
	for document in documents:
		document['_id'] = str(document['_id'])
		response.append(document)
	return response

def create(table,data):
	try:
		table.insert(data)
		data['_id'] = str(data['_id'])
		hasil = {
			'status' : 'sukses',
			'data' : data
		}
		return Response(json.dumps({"flag": True}),status=200, mimetype='application/json')
	except:
		return Response(json.dumps({"flag": False}), mimetype='application/json')
	
def read(table,parameter = None):
	try:
		if parameter == None:
			data = table.find()
		else:
			data = table.find(parameter)
		data = mongo2Json(data)
		return Response(json.dumps(data))
	except:
		return Response(json.dumps({"pesan": "Error"}), mimetype='application/json')


def update(table, parameter, data):
	try:
		table.update(parameter, data)
		return Response(status=200, mimetype='application/json')
	except:
		return Response(json.dumps({"pesan": "Error"}), mimetype='application/json')

def delete(table, parameter):
	try:
		table.delete_many(parameter)
		return Response(status=200, mimetype="application/json")
	except:
		return Response(json.dumps({"pesan": "Error"}), mimetype='application/json')


