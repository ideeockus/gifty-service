""" This module provides API common methods """
from flask import request, abort, Blueprint, current_app, jsonify
from models import OrderStatus, GoodsItem, GoodsCategory, Order, BoxType
from models import api

import json
import db

user_api = Blueprint("user_api", __name__, url_prefix="/api")


@user_api.post("/get_categories")
def get_goods_categories():
    categories = {category.name: category.value for category in GoodsCategory}
    current_app.logger.info(f"request for categories: {categories}")
    print(categories)
    response = json.dumps(categories)
    return response


@user_api.post("/get_goods_by_category")
def get_goods_by_category():
    req = api.GetGoodsByCategoryRequest(**request.json)
    # category = request.json.get('category')
    # if category not in [item.value for item in models.GoodsCategory]:
    #     abort(400, "wrong category")
    # category = models.GoodsCategory(req.category)
    current_app.logger.info(f"request for goods_by_category for {req.category}")
    # goods = [item.to_dict() for item in db.get_goods_by_category(req.category)]
    goods = db.get_goods_by_category(req.category)
    return jsonify(api.GetGoodsByCategoryResponse(
        goods=goods,
        status=api.ResponseStatus.Ok
    ))


@user_api.post("/create_order")
def create_order():
    req = api.CreateOrderRequest(**request.json)
    # goods_ids = request.json.get('goods_ids')
    # customer_name = request.json.get('customer_name')
    # customer_email = request.json.get('customer_email')
    # customer_address = request.json.get('customer_address')
    # customer_phone = request.json.get('customer_phone')
    # box_type = request.json.get('box_type')
    # comment = request.json.get('comment')

    # if None in (goods_ids, customer_name, customer_email, customer_address, customer_phone, box_type):
    #     abort(401, "Bad request")
    # if box_type not in [bt.value for bt in BoxType]:
    #     abort(401, "Invalid box type")

    # order: Order = Order(
    #     box_type=req.box_type,
    #     customer_name=req.customer_name,
    #     customer_email=req.customer_email,
    #     customer_phone=req.customer_phone,
    #     customer_address=req.customer_address,
    #     comment=req.comment
    # )

    order_id = db.create_new_order(
        box_type=req.box_type,
        customer_name=req.customer_name,
        customer_email=req.customer_email,
        customer_phone=req.customer_phone,
        customer_address=req.customer_address,
        comment=req.comment,
        goods_ids=req.goods_ids
    )

    return jsonify(api.CreateOrderResponse(
        status=api.ResponseStatus.Ok,
        order_id=order_id
    ))


@user_api.post("/get_order")
def get_order():
    req = api.GetOrderRequest(**request.json)
    # order_id = request.json.get('order_id')
    order = db.get_order_by_id(req.order_id)

    return jsonify(api.GetOrderResponse(
        order=order,
        status=api.ResponseStatus.Ok
    ))


@user_api.post("/get_order_status")
def get_order_status():
    req = api.GetOrderStatusRequest(**request.json)
    # order_id = request.json.get('order_id')
    order_status = db.get_order_status_by_id(req.order_id)

    return jsonify(api.GetOrderStatusResponse(
        order_status=order_status,
        status=api.ResponseStatus.Ok
    ))

