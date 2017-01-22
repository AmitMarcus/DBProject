#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
os.environ['PYTHON_EGG_CACHE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "python-eggs")

from flask import Flask, send_from_directory, jsonify, render_template, request, json, g
import decimal
import MySQLdb
import sys
import time

# Special encoder for decimal (jsonify has no support for decimal)
class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)
    
app = Flask(__name__)
app.json_encoder = MyJSONEncoder

def connect_db():
    MySQLConn = MySQLdb.connect('mysqlsrv.cs.tau.ac.il', 'DbMysql08', 'DbMysql08', 'DbMysql08', charset="utf8")
    MySQLConn.autocommit(True)

    return MySQLConn

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
        
# Serve static files like js, img, css etc.
@app.route('/<folder>/<fileName>')
def serveStatic(folder, fileName):
    if folder in ('js', 'img', 'css', 'lib', 'fonts', 'views', 'icons'):
        return send_from_directory(folder, fileName)
    
    return "404"

@app.route("/api/query/<query_name>/")
def query(query_name):
    if query_name in ("hottest_season.complex", "hottest_city.complex", "mosaic.complex", "most_popular_owners.complex"):
        sql = open("queries/" + query_name + ".sql").read()
        cur = connect_db().cursor(MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        return jsonify(cur.fetchall())
    
    return "404"

@app.route("/api/event/<id>/update/")
def eventUpdate(id):
    return "DONE"

@app.route("/api/event/<event_id>/")
def event(event_id):
    cur = connect_db().cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Event WHERE id = %s", (event_id,))
    event = cur.fetchone()
    return jsonify(event) 

@app.route("/api/event/<event_id>/comments/")
def comments(event_id):
    cur = connect_db().cursor(MySQLdb.cursors.DictCursor)
    sql = open("queries/comments_by_event.input.sql").read()
    cur.execute(sql, (event_id,))
    event = cur.fetchall()
    return jsonify(event)

@app.route("/api/event/<event_id>/comments/add/", methods=['POST'])
def addComment(event_id):
    json_data = request.get_json(force=True) 
    newComment = json_data['newComment']
    
    cur = connect_db().cursor(MySQLdb.cursors.DictCursor)
    sql = open("queries/new_comment_to_event.input.sql").read()
    cur.execute(sql, (newComment, event_id,))
    return "DONE"

@app.route("/api/search/", methods=['POST'])
def search():
    json_data = request.get_json(force=True) 
    searchString = json_data['searchString']

    cur = connect_db().cursor(MySQLdb.cursors.DictCursor)
    sql = open("queries/search.input.sql").read()
    print searchString
    print sql
    cur.execute(sql, (searchString,))
    event = cur.fetchall()
    return jsonify(event)

@app.route("/<path>")
@app.route("/<path>/")
def index(path):
	return send_from_directory("", "index.html")

@app.route("/")
def index2():
	return send_from_directory("", "index.html")

if __name__ == "__main__":
    port = 40666
    
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
        if port > 65535 or port < 0:
            print("Error: port range is 0 to 65535.")
            exit()
    elif len(sys.argv) > 2:
        print("Usage: Server.py [port]")
        exit()
        
    while True:
        try:
            app.run(host='0.0.0.0', port=port, threaded=True, debug=True)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            
        time.sleep(1)