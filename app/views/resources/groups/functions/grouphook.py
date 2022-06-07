
from flask import g
from flask import request
from flask import jsonify
from flask import abort

from app.views.auth.utils import auth_manager


class GROUPHOOKFunction:

    @classmethod
    def get(cls, group, *args, **kwargs): ... # Não Implementado

    
    @classmethod
    def multiple(cls, group:str, *args, **kwargs):
        match request.method:
            case "PUT": return cls.put( group )
            case "POST": return cls.post( group )
            case "DELETE": return cls.delete( group )
    
    @classmethod
    @auth_manager(require=True)
    def post(cls, group, *args, **kwargs):
        payload = request.form or request.get_json(silent=True)
        if payload is None: abort(400)
        u = payload.get("user", None)
        if u != g.user.id: abort(400)

        group = g.db.tables.getObjectById(group, code_error=404)
        if not group.members["ids"].count(g.user):
            if not group.entry: group.members = g.user
            else: group.solicitations = g.user
            return jsonify(group.to_dict(_medium=True)), 201
        return jsonify(group.to_dict(_medium=True))
        
    
    @classmethod
    @auth_manager(required=True)
    def put(cls, group, *args, **kwargs):
        
        payload = request.form or request.get_json(silent=True)
        if payload is None: abort(400)
        u = payload.get("user", None)
        if u is None: abort(400)

        u = g.db.tables.getObjectById(u)
        if u is None: abort(400)


        if u.id != g.user.id:
            gh = g.db.tables.GroupHook.query.filter_by(_user=g.user.id).first()
            if gh is None: abort(401)
            duty = {"member": 0, "mod": 1, "admin": 2, "owner": 3}
            if  duty.get(gh.duty) < 1: abort(401) # { 0: Member, 1: Mod, 2:Admin, 3: Owner}

        group = g.db.tables.getObjectById(group, code_error=404)
        if not group.members["ids"].count(u.id):
            group.members = u
            return jsonify(group.to_dict(_medium=True)), 201
        return jsonify(group.to_dict(_medium=True))
    
    @classmethod
    @auth_manager(require=True)
    def delete(cls, group, *args, **kwargs):
        u = request.form.get("user", None) or request.get_json(silent=True).get("user", None)
        if u is None: abort(400)


        if u != g.user.id:
            gh = g.db.tables.GroupHook.query.filter_by(_user=g.user.id, _group=group.id).first() # GroupHook
            if gh is None: abort(401)
            if gh.duty < 1: abort|(401) # { 0: Member, 1: Mod, 2:Admin, 3: Owner}
            u = g.db.tables.getObjectById(u)
        else: u = g.user

        
        group = g.db.tables.getObjectById(group, code_error=404)
        
        if group.members["ids"].count(u.id):
            if group.owners["ids"].count(u.id): abort(401)
            m = g.db.tables.GroupHook.query.filter_by(_user=u.id, _group=group.id).first()
            if m is None: abort(500)
            g.db.session.delete( m )
            g.db.session.commit()
            return jsonify(group.to_dict(_medium=True)),200 # membro deletado com sucesso
        
        elif group.solicitations["ids"].count(u.id):
            s = g.db.tables.Solicitation.query.filter_by(_req=u.id, _group=group.id).first()
            if s is None: abort(500)
            g.db.session.delete( s )
            g.db.session.commit()
            return jsonify(group.to_dict(_medium=True)),201 # solicitação deletada com sucesso


        return jsonify(group.to_dict(_medium=True)), 200 # ja deletou carai, atualiza sapoha ai