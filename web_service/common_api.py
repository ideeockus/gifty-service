import json

from flask import request, abort, Blueprint, current_app, jsonify, redirect

import models
import db

"""
This module provides API common methods
"""

api = Blueprint("api", __name__, url_prefix="/api")


@api.post("/get_categories")
def get_goods_categories():
    categories = {category.name: category.value for category in models.GoodsCategory}
    current_app.logger.info(f"request for categories: {categories}")
    response = json.dumps(categories)
    return response


@api.post("/get_goods_by_category")
def get_goods_by_category():
    category = request.json.get('category')
    if category not in [item.value for item in models.GoodsCategory]:
        abort(400, "wrong category")
    category = models.GoodsCategory(category)
    current_app.logger.info(f"request for goods_by_category for {category}")
    goods = [item.to_dict() for item in db.get_goods_by_category(category)]
    return jsonify(goods)


@api.post("/create_order")
def create_order():
    goods_ids = request.json.get('goods_ids')
    customer_name = request.json.get('customer_name')
    customer_email = request.json.get('customer_email')
    customer_address = request.json.get('customer_address')
    customer_phone = request.json.get('customer_phone')
    box_type = request.json.get('box_type')
    comment = request.json.get('comment')

    if None in (goods_ids, customer_name, customer_email, customer_address, customer_phone, box_type):
        abort(401, "Bad request")
    if box_type not in [bt.value for bt in models.BoxType]:
        abort(401, "Invalid box type")

    order: models.Order = models.Order(
        box_type=models.BoxType(box_type),
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone,
        customer_address=customer_address,
        comment=comment
    )

    order_id = db.create_new_order(order, goods_ids)

    return jsonify({"order_id": order_id})


@api.post("/get_order")
def get_order():
    order_id = request.json.get('order_id')
    order = db.get_order_by_id_as_dict(order_id)

    return jsonify(order)


@api.post("/get_order_status")
def get_order_status():
    order_id = request.json.get('order_id')
    order_status = db.get_order_status_by_id(order_id)

    return jsonify({"order_status": order_status})

