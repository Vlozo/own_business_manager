from main import app
from flask import jsonify, request, Response
from googleapiclient.errors import HttpError
from services import Manager
from storage import Storage
from time import localtime, strftime

SHEET_PATH = app.config.get('SHEET_PATH')

@app.route("/")
def home():
    return "Hello World!"

@app.route("/storage", methods=['POST'])
def storage_register_product():
    data = request.get_json()
    product = data.get('product')
    price = data.get("price")
    min_storage = data.get("min_storage")
    try:
        storage = Storage(SHEET_PATH)
        response = storage.register_product(product, price, min_storage)
        return response, 201
    
    except HttpError as err:
        return(err)

# Talvez seja mais correto em contexto isso ser um PUT
@app.route("/storage/add", methods=['POST'])
def storage_add_product():
    data = request.get_json()
    product = data.get("product")
    quantity = data.get("quantity")
    # No futuro, date vai ser recebida por uma automatização do front
    date = strftime("%d-%m-%Y %H:%M:%S", localtime())

    if not isinstance(quantity, int) or quantity <= 0:
        return "Invalid quantity", 400

    try:
        storage = Storage(SHEET_PATH)
        row_number = storage.manager.find_item_row("Storage!B2:B", product)
        if not row_number:
            return f"Failed to complete action, product {product} does not exists", 400
        
        stock_quantity = storage.manager.get_sheet_data(f"Storage!C{row_number}")
        stock_quantity = int(stock_quantity[0][0])
        response = storage.register_action(date, "ENTRADA", product, quantity)
        updated = storage.manager.update_data(f"Storage!C{row_number}", [(stock_quantity + quantity)])

        return response, 201
    
    except HttpError as err:
        return (err)

@app.route("/storage/sell", methods=['POST'])
def storage_sell_product():    
    data = request.get_json()
    product = data.get("product")
    quantity = data.get("quantity")
    discount = data.get("discount", 0)
    date = strftime("%d-%m-%Y %H:%M:%S", localtime())

    if not isinstance(quantity, int) or quantity <= 0:
        return "Invalid quantity", 400
    
    if not isinstance(discount, (int, float)) or discount < 0:
        return "Invalid discount", 400
    
    try:
        storage = Storage(SHEET_PATH)
        row_number = storage.manager.find_item_row("Storage!B2:B", product)
        if not row_number:
            return f"Failed to complete action, product {product} does not exists", 400

        stock_quantity = storage.manager.get_sheet_data(f"Storage!C{row_number}")
        stock_quantity = int(stock_quantity[0][0])
        if quantity > stock_quantity:
            return f"Failed to complete action, amount of selling ultrapass product amount in storage", 400
        
        movement = storage.register_action(date, "SAÍDA", product, quantity)
        updated = storage.manager.update_data(f"Storage!C{row_number}", [(stock_quantity - quantity)])
        response = storage.sell_product(product, quantity, discount) 

        return response, 201
    
    except HttpError as err:
        return (err)