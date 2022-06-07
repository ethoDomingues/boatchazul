from sqlalchemy.schema import Column
from sqlalchemy.types  import Integer
from sqlalchemy.types  import DateTime

from datetime import datetime
from datetime import timezone


class BaseTable:
    
    __tablename__ = None

    _id = Column(Integer, primary_key=True)
    created_at = Column( DateTime, default=datetime.now(timezone.utc) )


    @property
    def id(self): return f"{self.__tablename__}@{self._id}"

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items(): setattr(self, k, v)
    
