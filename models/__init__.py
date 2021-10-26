from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from markupsafe import escape
from enum import Enum, IntEnum
from sqlalchemy import Enum as sqlalchemyEnum

Base = declarative_base()  # декларативный базовый класс

# DbSession = sessionmaker(bind=engine, expire_on_commit=False)


class BoxSize(Enum):
    Mini = "Mini"
    Midi = "Midi"
    Bigi = "Bigi"


# class GoodsCategory(Enum):
#     Base = "Base"
#     Packet = "Packet"
#     Bonus = "Bonus"

class GoodsCategory(IntEnum):
    Base = 0
    Packet = 1
    Bonus = 2


# id | Name | Description | Category_id | Price | Path_img
class GoodsItem(Base):
    __tablename__ = "goods_items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category = Column(sqlalchemyEnum(GoodsCategory))
    price = Column(Float)
    img_path = Column(String)


# engine = create_engine(db_url, echo=False)
# Base.metadata.create_all(engine)
