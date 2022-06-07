from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask import abort


db = SQLAlchemy()

class Schema(dict):
    def __init__(self, **d_tables):
        dict.__init__(self, {})
        if d_tables:
            for n,t in d_tables.items():
                self[t.__tablename__] = t
                self.__setattr__(n, t)

        
    def getObjectById(self, id:str, code_error:int = None, **kwargs):
        if id is None: abort( 404 )
        id = id.split("@")
        if len(id) < 2: abort(400)
        

        t = self.get(id[0])
        if t:
            obj = t.query.filter_by(_id=id[1], **kwargs).first()
            if obj: return obj
        if code_error: abort(code_error)
        return

class Model:

    def __init__(self, app:"Flask") -> None:

        db.init_app(app)
        Migrate(app, db)
        app.db = db

        # IMPORT TABLES HERE
        from .tables.user import User
        from .tables.cdn import Cdn
        from .tables.react import React
        from .tables.comment import Comment
        from .tables.post import Post
        from .tables.post import Profile
        from .tables.friend import Friends
        from .tables.friend import Solicitation
        from .tables.group import Group
        from .tables.group import GroupHook

        db.tables = Schema(**{
            "Cdn": Cdn,
            "Post": Post,
            "User": User,
            "Group": Group,
            "React": React,
            "Comment": Comment,
            "Profile": Profile,
            "Friends": Friends,
            "GroupHook": GroupHook,
            "Solicitation": Solicitation,
        })
        
        
        
        
        

