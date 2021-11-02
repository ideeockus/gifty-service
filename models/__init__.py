from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from markupsafe import escape
from enum import Enum, IntEnum
from sqlalchemy import Enum as sqlalchemyEnum

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
    name = Column(String)
    description = Column(String)
    category = Column(sqlalchemyEnum(GoodsCategory))
    price = Column(Float)
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
    token = Column(String)
    expiration_date = Column(DateTime)


class OrderStatus(Enum):
    New = "New"
    Pending = "Pending"
    Processing = "Processing"
    Shipping = "Shipping"
    Done = "Done"


class Order(Base):
    __tablename__ = "oders"
    id = Column(Integer, primary_key=True)
    box_type = Column(sqlalchemyEnum(BoxType))
    status = Column(sqlalchemyEnum(OrderStatus))
    customer_name = Column(String)
    customer_email = Column(String)
    customer_phone = Column(String)
    customer_address = Column(String)
    creation_date = Column(DateTime)

