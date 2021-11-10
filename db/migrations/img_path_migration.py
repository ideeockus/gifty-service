from typing import List
from models import orm
from db import DbSession
from app_config import default_image_path


def apply_img_path_migration():
    print("Applying img_path migration")
    with DbSession.begin() as session:
        goods_orm: List[orm.GoodsItemORM] = session.query(orm.GoodsItemORM).all()
        for good_orm in goods_orm:
            if good_orm.img_path is None:
                good_orm.img_path = default_image_path


if __name__ == "__main__":
    apply_img_path_migration()