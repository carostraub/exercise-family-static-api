"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    if members:
        return jsonify(members), 200
    return jsonify ({"error":"Member not found"}), 400
   
@app.route('/member', methods=['POST'])
def add_member():
    data = request.json
    error = {}

    if not data.get("first_name"):
        error["first_name"] = "First name is required"
    if not data("age"):
        error["age"] = "Age is required"
    if not data.get("lucky_numbers"):
        error["lucky_numbers"] = "Lucky number is required"

    if error: 
        return jsonify({"error":error}), 400
    jackson_family.add_member(data)
    return jsonify({"msg":"New member added succefully"}), 200

@app.route('/member/<int:member_id>', methods=["GET"])
def get_member(member_id):
    member= jackson_family.get_member(member_id)
    if not member:
        return jsonify({"error":"This member doesn't exist"}), 400

    return jsonify(member), 200

@app.route('/member/<int:member_id>', methods=["DELETE"])
def delete_member(member_id):
    member= jackson_family.get_member(member_id)
    if member:
        jackson_family.delete_member(member_id)
        return jsonify({"done":True}), 200
    return jsonify({"error":"Member not found"}), 400

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
