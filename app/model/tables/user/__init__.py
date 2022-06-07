from sqlalchemy.schema import Column
from sqlalchemy.types import Date
from sqlalchemy.types import String

from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash    as cph

from app.model import db
from app.model.tables import BaseTable


class User(db.Model, BaseTable):

    __tablename__ = "users"

    birth = Column( Date, nullable=False )
    email = Column( String(64), nullable=False, unique=True )
    name = Column( String(64), nullable=False )
    username = Column( String(64), nullable=False, unique=True )
    
    _password = Column( String, nullable=False )

    

    @property
    def password( self ): raise AttributeError
    
    @password.setter
    def password( self, password:str ): self._password = gph( password )

    
    def check_password( self, password ): return cph( self._password, password )

    @property
    def profile(self): return db.tables.Profile.query.filter_by(_user=self.id, active=True).first()

    @profile.setter
    def profile(self, post):
        old = db.tables.Profile.query.filter_by(_user=self.id, active=True).first()
        if old:
            old.active = False
            db.session.add(old)
        profile = db.tables.Profile(user=self, post=post, img=post.pictures[0])
        db.session.add(profile)
        return    
    

    @property
    def all_profile(self): return db.tables.Profile.query.filter_by(_user=self.id).all()

    @all_profile.setter
    def all_profile(self, post):
        old = db.tables.Profile.query.filter_by(_user=self.id, active=True).first()
        if old:
            old.active = False
            db.session.add(old)
        profile = db.tables.Profile(user=self, post=post, img=post.pictures[0])
        db.session.add(profile)
        return    
    
    @property
    def groups(self):
        ghs = db.tables.GroupHook.query.filter_by(_user=self.id).all()
        gh_list = {"ids": [], "groups": []}
        for gh in ghs:
            gh_list["ids"].append(gh.group.id)
            gh_list["groups"].append(gh.group.to_dict())
        return gh_list
         
    @property
    def solicitations(self): return db.tables.Solicitation.get_solicitations( self.id )
        

    @property
    def friends(self): return db.tables.Friends.get_friends(self.id)
    
    def to_dict(self, _medium=False, _complete=False):

        data = {
            "id": self.id,
            "name": self.name,
            "profile": self.profile.to_dict() if self.profile else None,
            "username": self.username,
        }
        if _medium or _complete:
            data.update({
                "groups":  self.groups,
                "friends": self.friends,
                "solicitations": self.solicitations,
            })
        if _complete:
            data.update({
                "birth": self.birth,
                "created_at": self.created_at,
                "email": self.email,
                "all_profile": [ p.to_dict() for p in self.all_profile ],

            })
            

        return data