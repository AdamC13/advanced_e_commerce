from flask import Blueprint
from controllers.customerController import save, fetch_all
from services.customerService import delete_customer, update_customer

customer_blueprint = Blueprint("customer_bp", __name__)


customer_blueprint.route('/', methods=['POST'])(save)
customer_blueprint.route('/', methods=['GET'])(fetch_all)
customer_blueprint.route('/<customer_id>', methods=['PUT'])(update_customer)
customer_blueprint.route('/<customer_id>', methods=['DELETE'])(delete_customer)


