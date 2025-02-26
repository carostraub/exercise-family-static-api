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
    members = jackson_family.get_all_members()
    return jsonify(members), 200
    


@app.route('/member/<int:member_id>', methods=['GET'])
def member_id(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200


@app.route('/member', methods=['POST'])
def add_member():
    data = request.json
    required = ["first_name", "last_name", "age", "lucky_numbers"]
    if not all(field in data for field in required):
        return jsonify({"error": "All fields must be complete"}), 400
    
    new_member = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "age": data["age"],
        "lucky_numbers":data["lucky_numbers"]
    }
    jackson_family.add_member(new_member)
    return jsonify({"msg": "Family member added successfully"}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    errase = jackson_family.delete_member(member_id)
    if not errase:
        return jsonify({"error": "Family member not found"}), 404
    return jsonify({"msg": "Family member was deleted from history"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
