import json

from flask import request, abort, session, redirect, Blueprint, current_app, url_for, render_template
from typing import Optional

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
    return json.dumps(goods)
