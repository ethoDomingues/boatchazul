from sqlalchemy.schema import Column
from sqlalchemy.types import String
from sqlalchemy.types import Text
from sqlalchemy.types import JSON

from app.model import db
from app.model.tables import BaseTable


class Comment(db.Model, BaseTable):

    __tablename__ = "comments"

    content = Column( Text )
    _picture = Column( JSON )
    _owner = Column( String(64), nullable=False )# posts@123
    _user = Column( String(64), nullable=False )#  users@123

    @property
    def user(self): return db.tables.getObjectById(self._user)

    @user.setter
    def user(self, user): self._user = user.id


    @property
    def owner(self): return db.tables.getObjectById(self._owner)

    @owner.setter
    def owner(self, post): self._owner = post.id


    @property
    def picture(self ):
        if self._picture:
            return db.tables.getObjectById(self._picture)
    
    @picture.setter
    def picture(self, picture):
        if picture:
            self._picture =  picture.id

    @picture.deleter
    def picture(self):
        img =  self.picture
        if img: db.session.delete(img)

    
    @property
    def reacts(self):
        rs = db.tables.React.query.filter_by(owner=self.id).all()
        return [ r.user for r in rs ]
    
    @reacts.setter
    def reacts(self, user):
        obj = db.tables.React.query.filter_by(owner=self.id, user=user.id).first()
        if obj: db.session.delete(obj)
        else: db.session.add(db.tables.React(owner=self.id, user=user.id))
        db.session.commit()
    
    @reacts.deleter
    def reacts(self):
        for r in  db.tables.React.query.filter_by(owner=self.id).all(): db.session.delete(r)
        db.session.commit()



        

    def to_dict(self):


        return {
            "id": self.id,
            "user": self.user.to_dict(),
            "owner": self.owner.id,
            "content": self.content,
            "picture": self.picture.to_dict() if self.picture else None,
            "created_at": self.created_at,
            "reacts": self.reacts
        }