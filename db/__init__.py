"""
This module provides API to work with db
"""
from typing import List

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from app_config import db_url
from models import Base, GoodsItem, GoodsCategory
from flask import current_app


engine = create_engine(db_url, echo=False)
Base.metadata.create_all(engine)
DbSession = sessionmaker(engine)


def edit_goods_item(item: GoodsItem):
    with DbSession.begin() as session:  # DbSession.begin maintains a begin/commit/rollback block
        editing_item: GoodsItem = session.query(GoodsItem).filter(GoodsItem.id == item.id).scalar()
        current_app.logger.debug(editing_item)

        editing_item.name = item.name
        editing_item.description = item.description
        editing_item.price = item.price
        editing_item.img_path = item.img_path
        editing_item.category = item.category


def add_goods_item(item: GoodsItem):
    # with DbSession.begin() as session:  # DbSession.begin maintains a begin/commit/rollback block
    #     session
    current_app.logger.debug(f"adding goods_item {item}")
    session = DbSession()
    session.add(item)
    session.commit()
    session.close()


def del_goods_item_by_id(item_id: int):
    current_app.logger.debug(f"deleting goods_item id={item_id}")
    session = DbSession()
    item = session.query(GoodsItem).filter(GoodsItem.id == item_id)
    session.delete(item)
    session.commit()
    session.close()


def get_goods_by_category(category: GoodsCategory) -> List[GoodsItem]:
    session = DbSession()
    goods: List[GoodsItem] = session.query(GoodsItem).filter(GoodsItem.category == category).all()
    session.close()

    return goods



