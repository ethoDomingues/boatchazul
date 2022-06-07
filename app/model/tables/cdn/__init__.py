import base64
from sqlalchemy.schema import Column
from sqlalchemy.types import String
from sqlalchemy.types import LargeBinary
from sqlalchemy.types import JSON

from flask import url_for

from app.model import db
from app.model.tables import BaseTable



class Cdn(db.Model, BaseTable):

    __tablename__ = "cdn"

    body = Column( LargeBinary )
    owner = Column( String(64), nullable=False )
    headers = Column( JSON )
    filename = Column( String(64), nullable=False )

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "created_at": self.created_at,
            "url": self.url,
        }

    @property
    def url(self): return url_for("cdn.get", cdn=base64.urlsafe_b64encode(self.id.encode()), filename=self.filename, _external=True)