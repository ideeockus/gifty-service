from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from app_config import db_url
from markupsafe import escape
from enum import Enum
from sqlalchemy import Enum as sqlalchemyEnum

Base = declarative_base()  # декларативный базовый класс

# DbSession = sessionmaker(bind=engine, expire_on_commit=False)


class BoxSize(Enum):
    Mini = "Mini"
    Midi = "Midi"
    Bigi = "Bigi"


class GoodsCategory(Enum):
    Base = "Base"
    Packet = "Packet"
    Bonus = "Bonus"


# Name | Description | Category_id | Price | Path_img
class GoodsItem:
    __tablename__ = "goods_items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category = Column(sqlalchemyEnum(GoodsCategory))
    price = Column(Float)
    img_path = Column(String)


engine = create_engine(db_url, echo=False)
Base.metadata.create_all(engine)
