from typing import Optional, Union
from pydantic import BaseModel, FilePath, EmailStr, constr
from enum import Enum
from models import GoodsCategory

""" Models for API """


class ResponseStatus(Enum):
    Ok = "ok"
    Failed = "failed"


class CommonAdminRequest(BaseModel):
    auth_token: Optional[str]


class CommonResponse(BaseModel):
    status: ResponseStatus


# --------- admin api dataclasses ------------
class AdminSignInRequest(CommonAdminRequest):
    password: Optional[str]

class AdminSignInResponse(CommonResponse):
    auth_token: Optional[str]


class UploadPictureResponse(CommonResponse):
    img_path: str


class AddGoodsItemRequest(CommonAdminRequest):
    name: str
    description: Optional[str]
    price: Union[int, float]
    img_path: str = "/static/pictures/no_image.png"
    category: GoodsCategory

class AddGoodsItemResponse(CommonResponse):
    item_id: int


class EditGoodsItemRequest(CommonAdminRequest):
    item_id: int
    name: str
    description: Optional[str]
    price: Union[int, float]
    img_path: FilePath = "/static/pictures/no_image.png"
    category: GoodsCategory


class RemoveGoodsItemRequest(CommonAdminRequest):
    item_id: int
