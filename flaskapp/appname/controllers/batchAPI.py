from flask import Flask, jsonify, abort, request, session, Blueprint
from flask_restful import Resource, Api
from appname.models import (db, Batch)
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy

batchAPI = Blueprint('batchAPI', __name__)

@batchAPI.route('/addBatch', methods = ['POST'])

def add_batch():

        if not request.json or not 'name' in request.json:
                abort(400)

        b = Batch(request.json["name"], request.json["description"])

        db.session.add(b)

        db.session.commit()

        return jsonify( {'batch': b.serialize } ), 201

@batchAPI.route('/getBatch', methods = ['GET'])

def getBatch():
	return jsonify( json_list = [bt.serialize for bt in Batch.query.all()] )

