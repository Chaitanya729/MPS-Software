from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import json_util, ObjectId
from bson.json_util import dumps
from pymongo import MongoClient
import logging
import os
from werkzeug.utils import secure_filename
import base64

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

CONNECTION_STRING = "mongodb+srv://sandeepvetchaiitkgp:OG002q5Om7VOtcf7@sandy.0qlmpzm.mongodb.net/?retryWrites=true&w=majority&appName=sandy"
client = MongoClient(CONNECTION_STRING)
database_name = client['Motor_Parts']
collection_name = database_name["parts"]


# Get
@app.route("/api/parts", methods=['GET'])
def get_parts():
    parts = list(collection_name.find())
    for part in parts:
        part['image'] = base64.b64encode(part['image']).decode('utf-8')
    serialized_parts = json_util.dumps(parts)
    return serialized_parts


# Get
@app.route("/api/parts/<string:part_id>", methods=['GET'])
def get_part(part_id):
    part = collection_name.find_one({'_id': ObjectId(part_id)})
    if part:
        serialized_part = json_util.dumps(part)
        return serialized_part
    else:
        return jsonify({'message': 'Part not found'}), 404

# Put

@app.route("/api/parts/update/<string:part_id>", methods=['PUT'])
def update_part(part_id):
    try:
        # Get the new quantity value from the request body
        data = request.json
        temp = data.get('quantity')

        # Get the current quantity of the part
        part = collection_name.find_one({'_id': ObjectId(part_id)})
        current_quantity = part.get('quantity')

        # Calculate the new quantity by subtracting temp
        new_quantity = current_quantity - temp

        # Update the part in the database
        result = collection_name.update_one({'_id': ObjectId(part_id)}, {'$set': {'quantity': new_quantity}})

        if result.modified_count == 1:
            return jsonify({'message': 'Part updated successfully'}), 200
        else:
            return jsonify({'message': 'Part not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Search
@app.route('/api/search', methods=['GET'])
def search():
    print("I am called")
    query = request.args.get('query')
    parts = collection_name.find({"$or": [{"name": query}, {"_id": ObjectId(query) if ObjectId.is_valid(query) else None}]})
    for part in parts:
        # Convert the Binary image data to a base64 string
        part['image'] = base64.b64encode(part['image']).decode('utf-8')
    serialized_parts = json_util.dumps(parts)
    print(parts)
    return serialized_parts

# Delete
@app.route("/api/parts/remove/<string:part_id>", methods=['DELETE'])
def delete_part(part_id):
    try:

        result = collection_name.delete_one({'_id': ObjectId(part_id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Part removed successfully'}), 200
        else:
            return jsonify({'message': 'Part not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Add new items
@app.route('/api/add_item', methods=['POST'])
def add_item():
    try:
        name = request.form.get('name')
        weight = request.form.get('weight')
        height = request.form.get('height')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        status = request.form.get('status')

        if not weight or not height or not quantity or not price or not name:
            return jsonify({'message': 'Missing data: Ensure all fields are entered properly'})
        
        if 'image' not in request.files:
            return jsonify({'message': 'No image file provided'}), 400
        image = request.files['image']
        if image.filename == '':
            return jsonify({'message': "No selected file"}), 400  

        image_bianry = image.read()

        name = str(name)
        weight = float(weight)
        height = float(height)
        quantity = int(quantity)
        price = float(price)
        status = int(status)

        document = {
            'name': name,
            'weight': weight,
            'height': height,
            'quantity': quantity,
            'price': price,
            'image': image_bianry,
            'status': status
        }

        collection_name.insert_one(document)

        return jsonify({'message': 'Item added successfully!!!'}), 200
    except Exception as e:
        return jsonify({'message':str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = list(collection_name.find({"status": {"$ne": 0}}))
    for order in orders:
        order['image'] = base64.b64encode(order['image']).decode('utf-8')
    serialized_orders = json_util.dumps(orders)
    return serialized_orders 

@app.route("/api/makebill", methods=['POST'])
def make_bill():
    try:
        # Get the data from the request body
        data = request.json
        parts = data.get('parts')

        # Update the quantities of the parts in the database
        for part in parts:
            part_id = part['_id']
            quantity = part['quantity']
            part_doc = collection_name.find_one({'_id': ObjectId(part_id)})
            if not part_doc:
                return jsonify({'message': 'Part not found'}), 404
            current_quantity = part_doc.get('quantity')
            new_quantity = current_quantity - quantity
            collection_name.update_one({'_id': ObjectId(part_id)}, {'$set': {'quantity': new_quantity}})

        return jsonify({'message': 'Bill created successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    


if __name__ == "__main__":
    app.run(debug=True)