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
    categories = [category.name for category in models.GoodsCategory]
    # print(category)
    current_app.logger.info(f"request for categories: {categories}")
    response = json.dumps(categories)
    return response


@api.post("/get_goods_by_category")
def get_goods_by_category():
    category = request.json.get('category')
    current_app.logger.info(f"request for goods_by_category for {category}")
    goods = db.get_goods_by_category(category)
    return json.dumps(goods)
