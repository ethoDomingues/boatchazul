from sqlalchemy.schema import Column
from sqlalchemy.types import String

from app.model import db
from app.model.tables import BaseTable


class React(db.Model, BaseTable):

    __tablename__ = "reacts"

    user = Column( String(64), nullable=False )
    owner = Column( String(64), nullable=False )
