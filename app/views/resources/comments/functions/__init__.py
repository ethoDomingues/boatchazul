from flask import jsonify
from flask import abort
from flask import request
from flask import g

from app.views.auth.utils import auth_manager

from app.views.cdn.functions import CDNFunctions
from app.model.tables.comment import Comment


class COMMFunctions:

    @classmethod
    def multiple(cls, comm:str, *args, **kwargs):
        match request.method:
            case "GET": return cls.get( comm )
            case "PUT": return cls.put( comm )
            case "DELETE": return cls.delete( comm )

    @classmethod
    @auth_manager
    def get(cls, comm:str, *args, **kwargs): return jsonify( g.db.getObjectById(comm, code_error=404).to_dict() )

    @classmethod
    @auth_manager(required=True)
    def post(cls, *args, **kwargs):
        payload = request.form or request.get_json(silent=True)
        if payload is None: abort(400)
        print("to aqui")

        if "owner" not in payload: abort(400)
        post = g.db.tables.getObjectById(payload["owner"], code_error=400)


        f = request.files.get("image", None)
        if f: f = CDNFunctions.saveFile(f)[0]

        if payload or f:
            c = Comment(user=g.user, content=payload.get("content"), picture=f, owner=post)
            g.db.session.add(c)
            g.db.session.commit()

            return jsonify(**post.to_dict(),new_comment=c.to_dict())
        abort(400)


    @classmethod
    @auth_manager(required=True) 
    def put(cls, comm:str, *args, **kwargs):
        payload = request.form
        if not payload: payload = request.get_json(silent=True)

        if "owner" not in payload: abort(400)
        post = g.db.tables.getObjectById(payload["owner"], code_error=400)

        f = request.files.get("image", None)
        if f: f = CDNFunctions.saveFile(f)[0]

        if payload or f:
            c = Comment(user=g.user, content=payload.get("content"), picture=f, owner=post)
            g.db.session.add(c)
            g.db.session.commit()

            count = Comment.query.filter_by(owner=c.owner).count()
            return jsonify(**c.to_dict(),count=count)
        abort(400)


    @classmethod
    @auth_manager(required=True)
    def delete(cls, comm:str, *args, **kwargs):
        comm = g.db.tables.getObjectById(comm, code_error=404)
        p = comm.owner
        del comm.reacts
        del comm.picture
        g.db.session.delete(comm)
        g.db.session.commit()
        
        if p: return jsonify({"count": Comment.query.filter_by(_owner=p.id).count(), "id":p.id})
        return '', 204
    
            