from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import json_util
from bson import ObjectId
from pymongo import MongoClient
import logging
logging.basicConfig(level=logging.DEBUG)
import base64 
import os
import calendar
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import requests
import json

import datetime
from random import randrange

app = Flask(__name__)
CORS(app)

CONNECTION_STRING = "mongodb+srv://sandeepvetchaiitkgp:OG002q5Om7VOtcf7@sandy.0qlmpzm.mongodb.net/?retryWrites=true&w=majority&appName=sandy"
client = MongoClient(CONNECTION_STRING)
database_name = client['Motor_Parts']
collection_name = database_name["parts"]

collection1 = collection_name
db =database_name
collection2=db["sales"]

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
    if(query == ''):
        parts = list(collection_name.find())
        for part in parts:
            part['image'] = base64.b64encode(part['image']).decode('utf-8')
        serialized_parts = json_util.dumps(parts)
        return serialized_parts
    else :
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
        address = request.form.get('address')
        status = request.form.get('status')
        threshold = request.form.get('threshold')

        if not weight or not height or not quantity or not price or not name or not address:
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
        address = str(address)
        status = int(status)
        threshold = int(threshold)

        document = {
            'name': name,
            'weight': weight,
            'height': height,
            'quantity': quantity,
            'price': price,
            'address': address,
            'image': image_bianry,
            'status': status,
            'threshold': threshold
        }

        collection_name.insert_one(document)
        foundpart = collection_name.find_one(document)
        id = foundpart['_id']

        document_2 = {
            '_id': id,
            'name': name,
            'price': price
        }

        collection2.insert_one(document_2)

        return jsonify({'message': 'Item added successfully!!!'}), 200
    except Exception as e:
        return jsonify({'message':str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = list(collection_name.find({"status": 0}))
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
    
def get_todays_date():
    today = datetime.date.today()
    # print(type(today))
    return today

def get_dates_in_present_month():
    current_date = datetime.datetime.now()
    
    # Get the year and month of the current date
    year = current_date.year
    month = current_date.month
    
    # Get the number of days in the present month
    num_days = calendar.monthrange(year, month)[1]
    
    # Generate a list of dates for the present month
    dates_in_present_month = [str(datetime.date(year, month, day)) for day in range(1, num_days + 1)]
    
    
    return dates_in_present_month
def is_date_in_present_month(date_str):
    # Convert date string to datetime object
    given_date = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Get current year and month
    current_date = datetime.today()
    current_year = current_date.year
    current_month = current_date.month
    
    # Compare year and month components
    if given_date.year == current_year and given_date.month == current_month:
        return True
    else:
        return False

@app.route("/api/sales/<string:part_id>", methods=['PUT'])
def salesupdate(part_id):
    # part_id_str = str(part_id)
    try:
        data = request.json
        print(data)
        today = get_todays_date()
        q = data.get('quantity')


        mydict = collection2.find_one({'_id': ObjectId(part_id)})
        mypart = collection1.find_one({'_id': ObjectId(part_id)})
        print("Objects found")

        days=len(mydict)-3
        print(days)
        filter={'_id':ObjectId(part_id)}
        #updating threshold
        
        if(str(today) not in mydict.keys()):
         threshold=((mypart['threshold']*days)+data['quantity'])/(days+1)
         collection2.update_one(filter,{'$set': {str(today):q }})
        
        else:
         threshold=((mypart['threshold']*days)+data['quantity'])/(days)
         x=mydict[str(today)]+data['quantity']
         collection2.update_one(filter,{'$set': {str(today):x }})
        collection1.update_one(filter,{'$set': {'threshold': threshold}})    
        print(threshold)
        
        #updating Quantity
        #found_part=collection1.find_one({'_id':ObjectId(part_id)})
        #filter={'_id':ObjectId(part_id)}
        quantity=mypart['quantity']-data['quantity']
        print(quantity)
        update = {'$set': {'quantity': quantity}}
        collection1.update_one(filter,update)
        #updating status
        if(quantity < threshold):
            status=0
            print("Sadeep")
            collection1.update_one(filter,{'$set': {'status': status}})
        return 'succesfully updated'
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/revenueday')
def generate_pdf_revenue_sheet():
    print("Revenue day called")
    total_revenue = 0
    today_date=str(get_todays_date())
    output_file= today_date+'revenuesheet'+'.pdf'
    data = [["Part Name", "Sales Quantity", "Price per Unit", "Total Sales"]]
    query = {today_date: {"$exists": True}}
    sales=collection2.find(query)
    sales_data={}
    for part in sales:
       part_name=part["name"]
       part_price=part["price"]
       part_quantity=part[today_date]
       sales_data[part_name]=(part_quantity,part_price)
       
    
    for part, sales_info in sales_data.items():
        sales_quantity, price_per_unit = sales_info
        total_sales = sales_quantity * price_per_unit
        total_revenue += total_sales
        data.append([part, str(sales_quantity), f"${price_per_unit}", f"${total_sales}"])
    
    data.append(["Total Revenue", "", "", f"${total_revenue}"])

    doc = SimpleDocTemplate(output_file,pagesize=letter)
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    doc.build([table])
    os.system(f"start {output_file}")  # Works on Windows    
    return "sucess"  

@app.route('/revenuemonth')
def generate_month_sheet():
    print("Revenue month called")
    total_monthly_revenue = 0
    current_date = get_todays_date()
    present_month =current_date.month
    output_file= str(present_month)+'revenuesheet'+'.pdf'
    
    # Initialize data for the revenue sheet
    data = [["Date", "Total Sales"]]
    sales_data={}
    dates=get_dates_in_present_month()
    for date in dates:
       query={str(date): {"$exists": True}}
       parts=collection2.find(query)
       that_days_rev=0
       for part in parts:
          that_days_rev+=part[str(date)]*part['price']
       sales_data[str(date)]=that_days_rev   
       

    
    # Loop through each date in the sales data
    for date, daily_sales in sales_data.items():
        # Calculate total sales for the day
        
        total_monthly_revenue += daily_sales
        
        # Append date and total sales to the data list
        data.append([date, f"${daily_sales}"])
    
    # Add total monthly revenue to the data list
    data.append(["Total Monthly Revenue", f"${total_monthly_revenue}"])

    # Create PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    
    # Create table from data
    table = Table(data)
    
    # Define table style
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    
    # Apply table style
    table.setStyle(style)
    
    # Build PDF document with table
    doc.build([table])
    os.system(f"start {output_file}")  # Works on Windows    
    print(1)
    return "success"

@app.route('/graph/<string:part_id>')
def getChart(part_id):
 labels=[]
 values=[]
 part_sales=collection2.find_one({'name':part_id})
 del part_sales['_id']
 del part_sales['name']
 del part_sales['price']
 dates=get_dates_in_present_month()
 for date in dates:
    if(date in part_sales):
       labels.append(date)
       values.append(part_sales[date])
    else :
       labels.append(date)
       values.append(0)     
 #for key,value in part_sales.items():
  #  labels.append(key)
   # values.append(value)
 
 data={'labels':labels,'values':values}   
    
 print (data)
 return jsonify(data)

@app.route('/sales/gengraph', methods=['POST','GET'])
def gengraph():
   id=request.get_data()
   string_data = id.decode('utf-8')
   
   print(id)
  
   url = f' http://127.0.0.1:5000/graph/{string_data}'  
   reqdata=requests.get(url)
   print(reqdata.content)
   f=reqdata.content.decode('utf-8')
   dictionary_data = json.loads(f)
   print(dictionary_data)
   return jsonify(dictionary_data)

@app.route('/order/sendorder')
def send_orders():
    # Fetch the parts that need to be ordered
    parts = collection_name.find({"quantity": {"$lt": 7 * threshold}})

    # Prepare the data for the PDF
    data = [["Name", "ID", "Address", "Quantity"]]
    for part in parts:
        row = [part["name"], part["_id"], part["address"], 7 * threshold - part["quantity"]]
        data.append(row)

    # Create the PDF
    output_file = "orders.pdf"
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 14),

                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0,0), (-1,-1), 1, colors.black)])
    table.setStyle(style)
    doc.build([table])

    # Open the PDF (this will only work on Windows)
    os.system(f"start {output_file}")

    return "Success"

if __name__ == "__main__":
    app.run(debug=True)