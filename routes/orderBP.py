from flask import Blueprint
from controllers.orderController import save, fetch_all, view_order

order_blueprint = Blueprint("order_bp", __name__)


order_blueprint.route('/', methods=['POST'])(save)
order_blueprint.route('/', methods=['GET'])(fetch_all)
order_blueprint.route('/<order_id>', methods=['GET'])(view_order)

