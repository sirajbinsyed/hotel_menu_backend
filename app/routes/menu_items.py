from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.menu_item import MenuItem
from app import db

menu_items_bp = Blueprint('menu_items', __name__, url_prefix='/api/menu')

@menu_items_bp.route('', methods=['GET'])
def get_menu_items():
    items = MenuItem.query.all()
    return jsonify([{'id': i.id, 'name': i.name, 'description': i.description, 'price': i.price, 'category_id': i.category_id} for i in items]), 200

@menu_items_bp.route('/category/<int:categoryId>', methods=['GET'])
def get_items_by_category(categoryId):
    items = MenuItem.query.filter_by(category_id=categoryId).all()
    return jsonify([{'id': i.id, 'name': i.name, 'description': i.description, 'price': i.price, 'category_id': i.category_id} for i in items]), 200

@menu_items_bp.route('', methods=['POST'])
@jwt_required()
def create_menu_item():
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category_id = data.get('category_id')
    
    if not all([name, price, category_id]):
        return jsonify({'message': 'Name, price, and category_id are required'}), 400
    
    item = MenuItem(name=name, description=description, price=price, category_id=category_id)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Menu item created', 'id': item.id}), 201

@menu_items_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_menu_item(id):
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()
    item = MenuItem.query.get_or_404(id)
    
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    item.price = data.get('price', item.price)
    item.category_id = data.get('category_id', item.category_id)
    db.session.commit()
    return jsonify({'message': 'Menu item updated'}), 200

@menu_items_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_menu_item(id):
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({'message': 'Admin access required'}), 403
    
    item = MenuItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Menu item deleted'}), 200