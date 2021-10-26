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
    return models.GoodsCategory


@api.post("/get_goods_by_category")
def get_goods_by_category():
    category = request.json['category']
    current_app.logger.info(f"request for goods_by_category for {category}")
    goods = db.get_goods_by_category(category)
    return goods
