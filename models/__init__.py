from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from markupsafe import escape
from enum import Enum, IntEnum
from sqlalchemy import Enum as sqlalchemyEnum
from sqlalchemy.orm import relationship

Base = declarative_base()  # декларативный базовый класс

# DbSession = sessionmaker(bind=engine, expire_on_commit=False)


class BoxType(Enum):
    Mini = "mini"
    Midi = "midi"
    Bigi = "bigi"


# class GoodsCategory(Enum):
#     Base = "Base"
#     Packet = "Packet"
#     Bonus = "Bonus"

class GoodsCategory(IntEnum):
    Base = 1
    Packet = 2
    Bonus = 3


# id | Name | Description | Category_id | Price | Path_img
class GoodsItem(Base):
    __tablename__ = "goods_items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(sqlalchemyEnum(GoodsCategory), nullable=False)
    price = Column(Float, nullable=False)
    img_path = Column(String)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "img_path": self.img_path,
        }


# engine = create_engine(db_url, echo=False)
# Base.metadata.create_all(engine)

class AccountRole(Enum):
    Admin = 0
    User = 1


class AuthToken(Base):
    __tablename__ = "auth_tokens"
    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    expiration_date = Column(DateTime, nullable=False)


class OrderStatus(Enum):
    New = "New"
    Pending = "Pending"
    Processing = "Processing"
    Shipping = "Shipping"
    Done = "Done"


class OrdersGoodsAssociation(Base):
    __tablename__ = 'orders_goods_association'
    order_id = Column(ForeignKey('orders.id'), primary_key=True)
    goods_item_id = Column(ForeignKey('goods_items.id'), primary_key=True)
    goods_item = relationship("GoodsItem")
    goods_count = Column(Integer)

    def to_list(self) -> list:
        return [self.goods_item.to_dict()] * self.goods_count


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    box_type = Column(sqlalchemyEnum(BoxType), nullable=False)
    status = Column(sqlalchemyEnum(OrderStatus), nullable=False)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    customer_address = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    goods = relationship("OrdersGoodsAssociation")
    comment = Column(String)

    def to_dict(self) -> dict:
        print([goods_association.to_list() for goods_association in self.goods])
        goods = []
        for goods_association in (goods_association.to_list() for goods_association in self.goods):
            for goods_item in goods_association:
                goods.append(goods_item)
        return {
            "id": self.id,
            "box_type": self.box_type,
            "status": self.status.value if self.status is not None else None,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "customer_phone": self.customer_phone,
            "customer_address": self.customer_address,
            "creation_date": self.creation_date,
            "comment": self.comment,
            "goods": goods,
        }

