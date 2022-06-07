
from flask import jsonify
from flask import abort
from flask import g
from flask import request


from app.views.auth.utils import auth_manager


class GROUPFunctions:

    @classmethod
    @auth_manager(required=True)
    def get_all(cls,  *args, **kwargs):
        groups = g.db.tables.Group.query.order_by(g.db.tables.Group._id.desc()).all()
        return jsonify(groups=[ group.to_dict(_medium=True) for group in groups ])


    @classmethod
    def multiple(cls, group:str, *args, **kwargs):
        match request.method:
            case "GET": return cls.get( group )
            case "PUT": return cls.put( group )
            case "DELETE": return cls.delete( group )
    
    @classmethod
    @auth_manager(required=True)
    def get(cls, group, *args, **kwargs):
        return jsonify(g.db.tables.getObjectById(group, code_error=404).to_dict(_complete=True))


    @classmethod
    @auth_manager(required=True)
    def post(cls, *args, **kwargs):
        payload = request.form or request.get_json(silent=True)

        name = payload.get("name")
        entry = payload.get("entry")
        description = payload.get("description")
        if not name: abort(400)
        
        group = g.db.tables.Group.query.filter_by(name=name).first()
        if group is None:
            group = g.db.tables.Group(name=name, _owner = g.user.id, entry=entry, description=description)
            
            g.db.session.add(group)
            g.db.session.commit()

            group.owners = g.user
            group.members = g.user


            return jsonify(group.to_dict(_medium=True))
        return jsonify({"field": "name"}), 401

    @classmethod
    @auth_manager(required=True)
    def put(cls, group, *args, **kwargs): ...
    
    @classmethod
    @auth_manager(required=True)
    def delete(cls, group, *args, **kwargs):
        group =  g.db.tables.getObjectById( group )
        if group is None: abort( 400 )
        if not group.owners["ids"].count(g.user.id): abort( 401 )

        del group.posts
        del group.solicitations
        del group.members

        g.db.session.delete(group)
        g.db.session.commit()

        return "", 204
