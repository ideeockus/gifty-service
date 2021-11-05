"""
This module provides API to work with db
"""
from typing import List, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app_config import db_url
from models import GoodsItem, GoodsCategory, AccountRole, OrderStatus, Order, BoxType
from models import orm
from flask import current_app
from datetime import datetime, timedelta
from collections import Counter

import utils

engine = create_engine(db_url, echo=False)
orm.Base.metadata.create_all(engine)
# DbSession = sessionmaker(engine, expire_on_commit=False)
DbSession = sessionmaker(engine)


# ---------------- db user_api for GoodsItem -------------------------
def edit_goods_item(item: GoodsItem) -> bool:
    with DbSession.begin() as session:  # DbSession.begin maintains a begin/commit/rollback block
        editing_item: orm.GoodsItemORM = session.query(orm.GoodsItemORM).filter(orm.GoodsItemORM.id == item.id).scalar()
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
    item_orm = orm.GoodsItemORM(**item.dict())
    session = DbSession()
    session.add(item_orm)
    session.commit()
    item_id = item_orm.id
    session.close()

    return item_id


def del_goods_item_by_id(item_id: int) -> bool:
    current_app.logger.debug(f"deleting goods_item id={item_id}")
    session = DbSession()
    item = session.query(orm.GoodsItemORM).filter(orm.GoodsItemORM.id == item_id).scalar()
    if item is None:
        session.close()
        return False
    session.delete(item)
    session.commit()
    session.close()
    return True


def get_goods_by_ids(goods_ids: List[int]) -> List[GoodsItem]:
    session = DbSession()
    goods_orm: List[orm.GoodsItemORM] = session.query(orm.GoodsItemORM).filter(orm.GoodsItemORM.id.in_(goods_ids)).all()
    goods = ""
    session.close()

    return [GoodsItem.from_orm(goods_item_orm) for goods_item_orm in goods_orm]


def get_goods_by_category(category: GoodsCategory) -> List[GoodsItem]:
    session = DbSession()
    goods_orm: List[orm.GoodsItemORM] = session.query(orm.GoodsItemORM).filter(orm.GoodsItemORM.category == category).all()
    goods = [GoodsItem.from_orm(goods_item_orm) for goods_item_orm in goods_orm]
    session.close()

    return goods


# ------------------------- db user_api for AuthToken ----------------
def gen_new_auth_token() -> str:
    current_app.logger.debug(f"generating new auth token")
    session = DbSession()
    token = utils.gen_auth_token()
    expiration_date = datetime.utcnow() + timedelta(days=10)

    auth_token = orm.AuthTokenORM(
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
    is_valid = session.query(orm.AuthTokenORM).filter(orm.AuthTokenORM.token == token).scalar() is not None
    session.close()
    return is_valid


# ---------------------- db user_api for Order -----------------
# def create_new_order(order: Order, goods_ids: List[int]) -> int:
#     current_app.logger.debug(f"creating order {order}")
#     order_orm = orm.OrderORM(**order.dict())
#     if order_orm.creation_date is None:
#         order_orm.creation_date = datetime.utcnow()
#     order_orm.status = OrderStatus.New
#     goods = get_goods_by_ids(goods_ids)
#
#     goods_amount_by_id = Counter(goods_ids)
#
#     for goods_item in goods:
#         goods_association = orm.OrdersGoodsAssociationORM(goods_count=goods_amount_by_id[goods_item.id])
#         goods_association.goods_item = goods_item
#         order_orm.goods.append(goods_association)
#
#     session = DbSession()
#     session.add(order_orm)
#     order_id = order_orm.id
#     session.commit()
#     session.close()
#
#     return order_orm.id

def create_new_order(box_type: BoxType, customer_name: str, customer_email: str, customer_phone: str,
                     customer_address: str, comment: Optional[str], goods_ids: List[int]) -> int:
    current_app.logger.debug(f"Creating order")
    order_orm = orm.OrderORM(
        box_type=box_type,
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone,
        customer_address=customer_address,
        comment=comment,
        creation_date=datetime.utcnow(),
        status=OrderStatus.New
    )
    # if order_orm.creation_date is None:
    #     order_orm.creation_date = datetime.utcnow()
    # order_orm.status = OrderStatus.New
    session = DbSession()
    goods_orm: List[orm.GoodsItemORM] = session.query(orm.GoodsItemORM).filter(orm.GoodsItemORM.id.in_(goods_ids)).all()

    goods_amount_by_id = Counter(goods_ids)

    for goods_item in goods_orm:
        goods_association = orm.OrdersGoodsAssociationORM(goods_count=goods_amount_by_id[goods_item.id])
        goods_association.goods_item = goods_item
        order_orm.goods.append(goods_association)

    session.add(order_orm)
    session.commit()
    order_id = order_orm.id
    session.close()

    return order_id


# def get_order_by_id_as_dict(order_id: int) -> dict:
#     session = DbSession()
#     order = session.query(OrderORM).filter(OrderORM.id == order_id).scalar()
#     order_dict = order.to_dict()
#     session.close()
#
#     return order_dict

def get_order_by_id(order_id: int) -> Order:
    with DbSession() as session:
        order_orm = session.query(orm.OrderORM).filter(orm.OrderORM.id == order_id).scalar()
        order = Order.from_orm(order_orm)
        session.close()
        # print(order.dict())

        return order


def get_orders_by_status(order_status: OrderStatus) -> List[Order]:
    session = DbSession()
    orders_orm = list(session.query(orm.OrderORM).filter(orm.OrderORM.status == order_status).all())
    orders = [Order.from_orm(order_orm) for order_orm in orders_orm]
    session.close()

    return orders


def get_order_status_by_id(order_id: int) -> OrderStatus:
    session = DbSession()
    order = session.query(orm.OrderORM).filter(orm.OrderORM.id == order_id).scalar()
    session.close()

    return order.status


def set_order_status_by_id(order_id: int, order_status: OrderStatus) -> bool:
    session = DbSession()
    order = session.query(orm.OrderORM).filter(orm.OrderORM.id == order_id).scalar()
    order.status = order_status
    session.close()

    return True
