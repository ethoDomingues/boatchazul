from sqlalchemy.schema import Column
from sqlalchemy.types import String

from flask import abort

from app.model import db
from app.model.tables import BaseTable


class Friends(db.Model, BaseTable):

    __tablename__ = "friends"

    _user1 = Column( String(64), nullable=False )
    _user2 = Column( String(64), nullable=False )

    @property
    def user1(self): return db.tables.getObjectById(self._user1)

    @user1.setter
    def user1(self, user): self._user1 = user.id

    @property
    def user2(self): return db.tables.getObjectById(self._user2)

    @user2.setter
    def user2(self, user): self._user2 = user.id

    @classmethod
    def get_friends(cls, userBase ):
        f_list = {"ids": [], "users": []}
        
        f1 = cls.query.filter_by(_user1=userBase).all()
        f2 = cls.query.filter_by(_user2=userBase).all()

        for f in f1:
            f_list["ids"].append(f.user2.id)
            f_list["users"].append(f.user2.to_dict())

        for f in f2:
            f_list["ids"].append(f.user1.id)
            f_list["users"].append(f.user1.to_dict())

        return f_list



class Solicitation(db.Model, BaseTable):

    __tablename__ = "solicitations"

    _req = Column( String(64), nullable=False )
    _user = Column( String(64) )
    _group = Column( String(64 ))


    @property
    def req(self): return db.tables.getObjectById(self._req)

    @req.setter
    def req(self, user): self._req = user.id
    
    
    @property
    def user(self):
        if not self._user: raise AttributeError
        return db.tables.getObjectById(self._user)

    @user.setter
    def user(self, user): self._user = user.id

    @property
    def group(self):
        if not self._group: raise AttributeError
        return db.tables.getObjectById(self._group)

    @group.setter
    def group(self, group): self._group = group.id


    @classmethod
    def accept(cls, userReq, userAcc):

        sol1 = cls.query.filter_by(_req=userReq.id, _user=userAcc.id).first()
        sol2 = cls.query.filter_by(_req=userAcc.id, _group=userReq.id).first()


        if sol1 is None and sol2 is None: abort(500)
        
        if sol1:
            f = Friends(user1 = sol1.req, user2=sol1.user)
        elif sol2:
            f = sol2.members = sol2.req


        db.session.add(f)
        db.session.delete( sol1 or sol2 )
        db.session.commit()

        return f


    @classmethod
    def get_solicitations(cls, userBase ):
        if userBase.split("@")[0] == "users" :
            recs = [ u.req  for u in cls.query.filter_by(_user=userBase, _group=None).all() ]
            sens = [ u.user for u in cls.query.filter_by(_req=userBase, _group=None).all()]

            rec_list = { "ids": [], "users": [] }
            for user in recs:
                rec_list["ids"].append( user.id )
                rec_list["users"].append( user.to_dict() )

            sen_list = { "ids": [], "users": [] }
            for user in sens:
                sen_list["ids"].append( user.id )
                sen_list["users"].append( user.to_dict() )
            return {
                "received": rec_list,
                "sender": sen_list,
            }

        recs = [ s.req for s in cls.query.filter_by(_group=userBase).all() ]
        rec_list = { "ids": [], "users": [] }
        for user in recs:
            rec_list["ids"].append( user.id )
            rec_list["users"].append( user.to_dict() )

        return rec_list