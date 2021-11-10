from typing import List
from models import orm
from db import DbSession
from app_config import default_image_path

import os


def apply_img_path_migration():
    print("Applying img_path migration")
    with DbSession.begin() as session:
        goods_orm: List[orm.GoodsItemORM] = session.query(orm.GoodsItemORM).all()
        for good_orm in goods_orm:
            if good_orm.img_path is None:
                good_orm.img_path = default_image_path

            pictures_path = "static/pictures/"
            if pictures_path not in good_orm.img_path:
                new_img_path = os.path.join(pictures_path, good_orm.img_path) if \
                    good_orm.img_path[0] != "/" else pictures_path+good_orm.img_path[1:]
                good_orm.img_path = new_img_path


def apply_price_migration():
    print("Applying price migration")
    with DbSession.begin() as session:
        goods_orm: List[orm.GoodsItemORM] = session.query(orm.GoodsItemORM).all()
        for good_orm in goods_orm:
            if good_orm.price is None:
                session.delete(good_orm)
