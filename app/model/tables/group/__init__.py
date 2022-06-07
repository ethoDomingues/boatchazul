from sqlalchemy.schema import Column
from sqlalchemy.types import String
from sqlalchemy.types import Boolean


from app.model import db
from app.model.tables import BaseTable

from app.views.resources.posts.functions import POSTSFunctions


class Group(db.Model, BaseTable):
    __tablename__ = "groups"

    _owner = Column(String(64), nullable=False) # users@123
    
    name = Column(String(64), nullable=False, unique=True)
    entry = Column(Boolean, default=False)
    description = Column(String(64))

    ### PROPERTY ###

    @property
    def posts(self): return [ p.to_dict() for p in db.tables.Post.query.filter_by(_privacity=self.id).all() ]

    @posts.deleter
    def posts(self):
        ps = db.tables.Post.query.filter_by(_privacity=self.id).all()
        for p in ps: POSTSFunctions.del_post(post=p)


    @property
    def solicitations(self): return db.tables.Solicitation.get_solicitations( self.id )
    
    @solicitations.setter
    def solicitations(self, user):
        db.session.add(db.tables.Solicitation(group=self, req=user))
        db.session.commit()

    @solicitations.deleter
    def solicitations(self):
        sols = db.tables.Solicitation.query.filter_by(_group=self.id).all()
        for s in sols:
            db.session.delete(s)
        db.session.commit()

    @property
    def members(self):
        ghs = GroupHook.query.filter_by(_group=self.id).all()
        users, ids = [], []
        for gh in ghs:
            users.append(gh.user.to_dict())
            ids.append(gh.user.id)

        return {
            "users": users,
            "ids": ids
        }
    
    @members.setter
    def members(self, user):
        if GroupHook.query.filter_by(_group=self.id, _user=user.id).first() is None:
            sol = db.tables.Solicitation.query.filter_by(_group=self.id, _req=user.id).first()
            if sol: db.session.delete(sol)
            db.session.add(GroupHook(user=user, group=self))
            db.session.commit()

    @members.deleter
    def members(self):
        ghs = db.tables.GroupHook.query.filter_by(_group=self.id).all()
        if ghs:
            for gh in ghs: db.session.delete(gh)
        db.session.commit()

    @property
    def mods(self):
        ghs = db.tables.GroupHook.query.filter_by(_group=self.id, duty="mod").all()
        users, ids = [], []
        for gh in ghs:
            users.append(gh.user.to_dict())
            ids.append(gh.user.id)

        return {
            "users": users,
            "ids": ids
        }

    @mods.setter
    def mods(self, user):
        gh = db.tables.GroupHook.query.filter_by(_group=self.id, _user=user.id).first()
        gh.duty = "mod"
        db.session.add(gh)
        db.session.commit()

    @property
    def admins(self):
        ghs = db.tables.GroupHook.query.filter_by(_group=self.id, duty="admin").all()
        users, ids = [], []
        for gh in ghs:
            users.append(gh.user.to_dict())
            ids.append(gh.user.id)

        return {
            "users": users,
            "ids": ids
        }
    
    @admins.setter
    def admins(self, user):
        gh = db.tables.GroupHook.query.filter_by(_group=self.id, _user=user.id).first()
        gh.duty = "admin"
        db.session.add(gh)
        db.session.commit()
    
    
    @property
    def owners(self):
        ghs = db.tables.GroupHook.query.filter_by(_group=self.id, duty="owner").all()
        users, ids = [], []
        for gh in ghs:
            users.append(gh.user.to_dict())
            ids.append(gh.user.id)
        
        return {
            "users": users,
            "ids": ids
        }

    @owners.setter
    def owners(self, user):
        self._owner = user.id
        gh = db.tables.GroupHook.query.filter_by(_group=self.id, _user=user.id).first()
        if gh is None: gh = db.tables.GroupHook(group=self, user=user)
        gh.duty = "owner"
        db.session.add(gh)
        db.session.commit()

    ### METHOD ###

    def to_dict(self, _medium=False, _complete=False):
        resp =  {
            "id": self.id,
            "name": self.name,
            "entry": self.entry,
            "description": self.description,
        }
        if _medium or _complete:
            resp.update({
                "mods": self.mods,
                "owners": self.owners,
                "admins": self.admins,
                "members": self.members,
                "solicitations": self.solicitations,
            })
        if _complete: resp.update({ "posts": self.posts })
        return resp



class GroupHook(db.Model, BaseTable):
    __tablename__ = "groupshook"

    _user = Column(String(64), nullable=False) # users@123
    _group = Column(String(64), nullable=False) # groups@123
    duty = Column(String(64), nullable=False, default="mem") # adm, mod, mem

    @property
    def user(self): return db.tables.getObjectById(self._user )

    @user.setter
    def user(self, user): self._user = user.id
    
    @property
    def group(self): return db.tables.getObjectById(self._group)

    @group.setter
    def group(self, group): self._group = group.id


    def to_dict(self):
        {
            "id": self.id,
            "user": self.user.to_dict(),
            "group": self.group,
            "duty": self.duty,
        }

