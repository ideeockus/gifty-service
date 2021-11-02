"""
This module provides API to work with db
"""
from typing import List

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from app_config import db_url
from models import Base, GoodsItem, GoodsCategory, AuthToken, AccountRole, Order, OrderStatus, OrdersGoodsAssociation
from flask import current_app
from datetime import datetime, timedelta
from collections import Counter
import utils

engine = create_engine(db_url, echo=False)
Base.metadata.create_all(engine)
DbSession = sessionmaker(engine, expire_on_commit=False)


# ---------------- db api for GoodsItem -------------------------
def edit_goods_item(item: GoodsItem) -> bool:
    with DbSession.begin() as session:  # DbSession.begin maintains a begin/commit/rollback block
        editing_item: GoodsItem = session.query(GoodsItem).filter(GoodsItem.id == item.id).scalar()
        if editing_item is None:
            return False
        current_app.logger.debug(editing_item)

        editing_item.name = item.name
        editing_item.description = item.description
        editing_item.price = item.price
        editing_item.img_path = item.img_path
        editing_item.category = item.category
        return True


def add_goods_item(item: GoodsItem) -> int:
    # with DbSession.begin() as session:  # DbSession.begin maintains a begin/commit/rollback block
    #     session
    current_app.logger.debug(f"adding goods_item {item}")
    session = DbSession()
    session.add(item)
    session.commit()
    session.close()

    return item.id


def del_goods_item_by_id(item_id: int) -> bool:
    current_app.logger.debug(f"deleting goods_item id={item_id}")
    session = DbSession()
    item = session.query(GoodsItem).filter(GoodsItem.id == item_id).scalar()
    if item is None:
        return False
    session.delete(item)
    session.commit()
    session.close()
    return True


def get_goods_by_ids(goods_ids: List[int]) -> List[GoodsItem]:
    session = DbSession()
    goods: List[GoodsItem] = session.query(GoodsItem).filter(GoodsItem.id.in_(goods_ids)).all()
    session.close()

    return goods


def get_goods_by_category(category: GoodsCategory) -> List[GoodsItem]:
    session = DbSession()
    goods: List[GoodsItem] = session.query(GoodsItem).filter(GoodsItem.category == category).all()
    session.close()

    return goods


# ------------------------- db api for AuthToken ----------------
def gen_new_auth_token() -> str:
    current_app.logger.debug(f"generating new auth token")
    session = DbSession()
    token = utils.gen_auth_token()
    expiration_date = datetime.utcnow() + timedelta(days=10)

    auth_token = AuthToken(
        token=token,
        expiration_date=expiration_date,
    )
    session.add(auth_token)
    session.commit()
    session.close()
    return token


def validate_authorization(token: str) -> bool:
    current_app.logger.debug(f"validating token")
    session = DbSession()
    is_valid = session.query(AuthToken).filter(AuthToken.token == token).scalar() is not None
    session.close()
    return is_valid


# ---------------------- db api for order creation -----------------
def create_new_order(order: Order, goods_ids: List[int]) -> int:
    current_app.logger.debug(f"creating order {order}")
    if order.creation_date is None:
        order.creation_date = datetime.utcnow()
    order.status = OrderStatus.New
    goods = get_goods_by_ids(goods_ids)

    goods_amount_by_id = Counter(goods_ids)

    for goods_item in goods:
        goods_association = OrdersGoodsAssociation(goods_count=goods_amount_by_id[goods_item.id])
        goods_association.goods_item = goods_item
        order.goods.append(goods_association)

    session = DbSession()
    session.add(order)
    session.commit()
    session.close()

    return order.id


def get_order_by_id_as_dict(order_id: int) -> dict:
    session = DbSession()
    order = session.query(Order).filter(Order.id == order_id).scalar()
    order_dict = order.to_dict()
    session.close()

    return order_dict


def get_orders_by_status(order_status: OrderStatus) -> List[Order]:
    session = DbSession()
    orders = list(session.query(Order).filter(Order.status == order_status).all())
    session.close()

    return orders


def get_order_status_by_id(order_id: int) -> OrderStatus:
    session = DbSession()
    order = session.query(Order).filter(Order.id == order_id).scalar()
    session.close()

    return order.status


def set_order_status_by_id(order_id: int, order_status: OrderStatus) -> bool:
    session = DbSession()
    order = session.query(Order).filter(Order.id == order_id).scalar()
    order.status = order_status
    session.close()

    return True
