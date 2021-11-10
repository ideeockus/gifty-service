from pydantic import BaseModel, validator
from enum import Enum, IntEnum
from typing import Union, Optional, List
from datetime import datetime
from app_config import orders_comment_max_length, default_image_path


class BoxType(Enum):
    Mini = "mini"
    Midi = "midi"
    Bigi = "bigi"


class GoodsCategory(IntEnum):
    Base = 1
    Packet = 2
    Bonus = 3


class OrderStatus(Enum):
    New = "New"
    Pending = "Pending"
    Processing = "Processing"
    Shipping = "Shipping"
    Done = "Done"


class AccountRole(Enum):
    Admin = 0
    User = 1


class GoodsItem(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    category: GoodsCategory
    price: Union[int, float]
    img_path: str = default_image_path

    class Config:
        orm_mode = True
    #     validate_assignment = True
    #
    # @validator('img_path')
    # def set_name(cls, img_path):
    #     return img_path or default_image_path


class AuthToken(BaseModel):
    id: Optional[int]
    token: str
    expiration_date: datetime

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: Optional[int]
    box_type: BoxType
    status: OrderStatus = OrderStatus.New
    customer_name: str
    customer_email: str
    customer_phone: str
    customer_address: str
    creation_date: datetime
    goods: List[GoodsItem]
    comment: Optional[str]

    class Config:
        orm_mode = True

    # @validator("*", pre=True)
    # def evaluate_lazy_columns(cls, v):
    #     if isinstance(v, Query):
    #         return v.all()
    #     return v
    @validator("goods", pre=True)
    def evaluate_lazy_goods(cls, goods_orm):
        goods = list()
        for goods_association in goods_orm:
            if isinstance(goods_association, GoodsItem):
                return goods_association
            goods_items = filter(
                lambda gi: gi is not None,
                [goods_association.goods_item] * goods_association.goods_count
            )
            goods.extend(goods_items)
        return goods
