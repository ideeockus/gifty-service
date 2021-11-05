""" Models for API """

from typing import Optional, Union, List
from pydantic import BaseModel, Field
from enum import Enum
from models import GoodsCategory, GoodsItem, BoxType, OrderStatus, Order


class ResponseStatus(Enum):
    Ok = "ok"
    Failed = "failed"


# class CommonAdminRequest(BaseModel):
#     auth_token: Optional[str]

class AuthTokenHeader(BaseModel):
    auth_token: Optional[str] = Field(alias="Auth-Token")


class CommonResponse(BaseModel):
    status: ResponseStatus


# --------- admin user_api dataclasses ------------
class AdminSignInRequest(BaseModel):
    password: Optional[str]
class AdminSignInResponse(CommonResponse):
    auth_token: Optional[str]


class UploadPictureResponse(CommonResponse):
    img_path: str


class AddGoodsItemRequest(BaseModel):
    name: str
    description: Optional[str]
    price: Union[int, float]
    img_path: str = "/static/pictures/no_image.png"
    category: GoodsCategory
class AddGoodsItemResponse(CommonResponse):
    item_id: int


class EditGoodsItemRequest(BaseModel):
    item_id: int
    name: str
    description: Optional[str]
    price: Union[int, float]
    img_path: str = "/static/pictures/no_image.png"
    category: GoodsCategory


class RemoveGoodsItemRequest(BaseModel):
    item_id: int


# ---------- user user_api dataclasses --------

class GetGoodsByCategoryRequest(BaseModel):
    category: GoodsCategory
class  GetGoodsByCategoryResponse(CommonResponse):
    goods: List[GoodsItem]


class CreateOrderRequest(BaseModel):
    box_type: BoxType
    customer_name: str
    customer_email: str
    customer_phone: str
    customer_address: str
    comment: Optional[str]
    goods_ids: List[int]
class  CreateOrderResponse(CommonResponse):
    order_id: int


class GetOrderRequest(BaseModel):
    order_id: int
class GetOrderResponse(CommonResponse):
    order: Order


class GetOrderStatusRequest(BaseModel):
    order_id: int
class GetOrderStatusResponse(CommonResponse):
    order_status: OrderStatus


