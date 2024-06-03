from flask import request, jsonify
from schemas.customerSchema import customer_schema, customers_schema
from services import customerService
from marshmallow import ValidationError


def save():
    try:
        # Validaate and deserialize the request data
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # Call the save service with the customer data
    customer_save = customerService.save(customer_data)
    # Serialize the customer data and return with a 201 success
    return customer_schema.jsonify(customer_save), 201

def fetch_all():
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    customers = customerService.find_all(page, per_page)
    return customers_schema.jsonify(customers)


