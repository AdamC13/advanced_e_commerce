from flask import Blueprint
from controllers.productController import save, fetch_all
from services.productService import delete_product, update_product

product_blueprint = Blueprint("product_bp", __name__)


product_blueprint.route('/', methods=['POST'])(save)
product_blueprint.route('/', methods=['GET'])(fetch_all)
product_blueprint.route('/<product_id>', methods=['PUT'])(update_product)
product_blueprint.route('/<product_id>', methods=['DELETE'])(delete_product)
