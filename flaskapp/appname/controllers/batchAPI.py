from flask import Flask, jsonify, abort, request, session, Blueprint
from flask_restful import Resource, Api
from appname.models import (db, Batch, Result, DataSet, Implementation, Algorithm, Argument)
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy

batchAPI = Blueprint('batchAPI', __name__)

@batchAPI.route('/addBatch/<int:id>/', methods = ['POST'])

def add_batch(id):

        if not request.json:
               return "File must be json to be submitted to database"

	temp = Batch.query.get(id)  

	if temp is None:
		return "Batch " + id + " was not found in the database"

	results = Result(id, json.request) 

        db.session.add(results)

        db.session.commit()

        return "Success!" 

@batchAPI.route('/getBatch/<int:id>/', methods = ['GET'])

def getBatch(id):
	b = Batch.query.get(id)
	if b is None:
		return "Batch " + id + " was not found in database"

	d = DataSet.query.get(b.data_set_idx)	
	
	i = Implementation.query.get(b.implementation_idx)

	a = Algorithm.query.get(i.algorithm_idx)

#	args = [arg.serialize for arg in i.argumentsx]

	#final_b = {b.serialize, d.serialize, i.serialize, a.serialize}

	return jsonify(b.serialize)
