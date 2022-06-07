

from flask import g
from flask import request
from flask import jsonify
from flask import abort

from app.model.tables.friend import Friends
from app.model.tables.friend import Solicitation
from app.views.auth.utils import auth_manager





class FRIENDSFunction:

    @classmethod
    def multiple(cls, user:str, *args, **kwargs):
        match request.method:
            case "GET": return cls.get( user )
            case "PUT": return cls.put( user )
            case "DELETE": return cls.delete( user )


    @classmethod
    @auth_manager(require=True )
    def post(cls, *args, **kwargs ):
        payload = request.form or request.get_json(silent=True)

        u = g.db.tables.getObjectById(payload.get("user"), code_error=400)

        s_temp = Solicitation.query.filter_by(_req=u.id, _user=g.user.id).first()
        if not s_temp:
            s_temp = Solicitation.query.filter_by(_req=g.user.id, _user=u.id).first()
            if not s_temp:

                s = Solicitation(req=g.user, user=u)

                g.db.session.add(s)
                g.db.session.commit()
            
                return "", 201
        return "", 200
    
    @classmethod
    @auth_manager
    def get(cls, user, *args, **kwargs ): return jsonify(g.db.tables.Friends.get_friends(user, _dict=True))

    @classmethod
    @auth_manager( require=True )
    def put(cls, *args, **kwargs ): 
        payload = request.form or request.get_json(silent=True)
        u = g.db.tables.getObjectById(payload.get("user"), code_error=400)
        Solicitation.accept(userReq=u, userAcc=g.user)
        g.db.session.commit()
        return "", 201
    
    @classmethod
    @auth_manager( require=True )
    def delete(cls, *args, **kwargs ):
        payload = request.form or request.get_json(silent=True)
        u = g.db.tables.getObjectById(payload.get("user"), code_error=400)
        f = Friends.query.filter_by(_user1=u.id, _user2=g.user.id).first() or \
            Friends.query.filter_by(_user1=g.user.id, _user2=u.id).first()
        if f is None:
            f = Solicitation.query.filter_by(_req=g.user.id, _user=u.id).first()
            if f is None:
                abort(400)
        g.db.session.delete(f)
        g.db.session.commit()
        return "", 204