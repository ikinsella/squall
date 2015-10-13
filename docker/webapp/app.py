from flask import Flask, redirect, url_for, request, render_template
import datetime
import os
from pymongo import MongoClient

app = Flask(__name__)

# Make connection to DB container
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.post_database

"""
@app.route('/')
def hello():
    client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
    db = client.post_database
    posts = db.posts
    post = {"Hello": "Hello World!",
            "text": "This page was viewed at",
            "date": datetime.datetime.utcnow()}
    newest_post_id = posts.insert_one(post).inserted_id
    mystr = "start\n"
    for post in posts.find():
        mystr = mystr + str(post) + "\n"
    #  newest_post = posts.find_one({"_id": str_id})
    #  return str(posts.find_one({"_id": newest_post_id}))
    return mystr
"""

@app.route('/')
def todo():
    _experiments = db.experiments.find()
    experiments = [experiment for experiment in _experiments]
    return render_template('squall.html', items=experiments)

@app.route('/new', methods=['POST'])
def new():
    item_doc = {'name': request.form['name'],
                'description': request.form['description']}
    db.experiments.insert_one(item_doc)
    return redirect(url_for('todo'))
            
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
