from typing import Optional, Union
from pydantic import BaseModel, FilePath, EmailStr, constr, Field
from enum import Enum
from models import GoodsCategory

""" Models for API """


class ResponseStatus(Enum):
    Ok = "ok"
    Failed = "failed"


# class CommonAdminRequest(BaseModel):
#     auth_token: Optional[str]

class AuthTokenHeader(BaseModel):
    auth_token: Optional[str] = Field(alias="Auth-Token")


class CommonResponse(BaseModel):
    status: ResponseStatus


# --------- admin api dataclasses ------------
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
    img_path: FilePath = "/static/pictures/no_image.png"
    category: GoodsCategory


class RemoveGoodsItemRequest(BaseModel):
    item_id: int

# ---------- user api dataclasses --------


