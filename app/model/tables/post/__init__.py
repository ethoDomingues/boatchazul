
from sqlalchemy.schema import Column
from sqlalchemy.types import String
from sqlalchemy.types import Text
from sqlalchemy.types import JSON
from sqlalchemy.types import Boolean

from flask import abort

from app.model import db
from app.model.tables import BaseTable


PRIVACITY_DATA = {
     "friends": "Amigos",
     "public": "Público"
    }


class Post(db.Model, BaseTable):

    __tablename__ = "posts"

    content = Column( Text )#........................... texto ou None
    deleted = Column( Boolean, default=0 )#............. bool
    
    _user = Column( String(64), nullable=False )#....... users@123
    _shared = Column( String(64), default=None )#....... id post original
    _pictures = Column( JSON )#......................... [ 12, 13, 14 ] or None
    _privacity = Column( String(64) )#.................. public | friends | groups@123
    # settings = Column( JSON )#........................ {"data": "data"}
    

    ### PROPERTY ###

    @property
    def privacity(self):
        if self._privacity in ["public", "friends"]: return self._privacity
        return db.tables.getObjectById(self._privacity)
    
    @privacity.setter
    def privacity(self, p): self._privacity = p
    
    @property
    def user(self): return db.tables.getObjectById(self._user)

    @user.setter
    def user(self, user): self._user = user.id

    @property
    def shared(self):
        if self._shared:
            p_sh = db.tables.getObjectById(self._shared)
            if p_sh is None: return
            p_sh.count = self.query.filter_by(_shared=self._shared).count()
            return p_sh
        return

    @shared.setter
    def shared(self, post): self._shared = post.id

    @property
    def pictures(self ):
        imgs = []
        if self._pictures:
            for f in self._pictures:
                i = db.tables.getObjectById(f)
                if i: imgs.append(i)
        return imgs
    
    @pictures.setter
    def pictures(self, pictures:list):
        
        self._pictures = [ p.id for p in pictures ]
        print(self._pictures)
    
    @pictures.deleter
    def pictures(self):
        for pic in self.pictures: db.session.delete(pic)
        db.session.commit()


    @property
    def comments(self): return db.tables.Comment.query.filter_by( _owner=self.id ).order_by( db.tables.Comment._id.desc()).all()
    
    @comments.setter
    def comments(self, comm): ...
    
    @comments.deleter
    def comments(self):
        for c in self.comments:
            db.session.delete(c)
        db.session.commit()
    
    @property
    def reacts(self): return [ r.user for r in db.tables.React.query.filter_by(owner=self.id).all() ]
    
    @reacts.setter
    def reacts(self, user):
        obj = db.tables.React.query.filter_by(owner=self.id, user=user.id).first()
        if obj: db.session.delete(obj)
        else: db.session.add(db.tables.React(owner=self.id, user=user.id))
        db.session.commit()
    
    @reacts.deleter
    def reacts(self):
        reacts = db.tables.React.query.filter_by(owner=self.id).all()
        for r in reacts: db.session.delete(r)
        db.session.commit()

    @property
    def profile(self): return db.tables.Profile.query.filter_by(_post=self.id, _user=self.user.id).first()

    @profile.deleter
    def profile(self):
        pf = self.profile
        if pf is None: return
        db.session.delete(pf)
        db.session.commit()
        return
    
    ### METHOD ###

    def self_delete(self):
        del self.pictures
        del self.comments
        del self.reacts
        del self.profile            

        if Post.query.filter_by(_shared=self.id).count(): # esse post foi compartilhado
            self.content = None
            self.deleted = True
            self._pictures = None
            db.session.add(self)

        elif self._shared: # esse post é um compartilhamento
            l_sh = Post.query.filter_by(_shared=self._shared).count()
            if l_sh == 1:
                sh = Post.query.filter_by(_id=self._shared.split("@")[1]).first()
                if sh.deleted: db.session.delete(sh)
            db.session.delete(self)
        else:
            db.session.delete(self)
        db.session.commit()
        return

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.to_dict(),
            "shared": self.shared.to_dict() if self.shared else None,
            "reacts": self.reacts,
            "deleted": self.deleted,
            "content": self.content,
            "profile": self.profile.to_dict() if self.profile else None,
            "privacity": self.privacity.to_dict() if isinstance(self.privacity, db.tables.Group) else self._privacity,
            "pictures": [p.to_dict() for p in self.pictures],
            "comments": [c.to_dict() for c in self.comments],
            "created_at": self.created_at,
        }


class Profile(db.Model, BaseTable):


    __tablename__ = "profiles"

    _img =  Column( String(64), nullable=False ) # cdn@123
    _post = Column( String(64), nullable=False ) # posts@123
    _user = Column( String(64), nullable=False ) # users@123
    active = Column( Boolean, nullable=False, default=1 )

    @property
    def user(self): return db.tables.getObjectById(self._user)

    @user.setter
    def user(self, user): self._user = user.id
    
    @property
    def post(self): return db.tables.getObjectById(self._post)

    @post.setter
    def post(self, post): self._post = post.id


    @property
    def img(self): return db.tables.getObjectById(self._img)

    @img.setter
    def img(self, img): self._img = img.id


    def to_dict(self):
        return {
            "id": self.id,
            "img": self.img.to_dict(),
            "active": self.active,
            "post_id": self._post,
            "user_id": self._user,
        }