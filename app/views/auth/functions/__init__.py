import base64

import datetime

from flask import abort
from flask import url_for
from flask import jsonify
from flask import render_template

from flask import request
from flask import session
from flask import g


from app.views.auth.utils import create_access_jwt
from app.views.auth.utils import auth_manager

from app.model.tables.user import User



class AUTHFunctions:


    @classmethod
    def login_multiple(cls):
        match request.method:
            case "GET": return cls.login_get()
            case "POST": return cls.login_post()
            case "DELETE": return cls.login_delete()
    
    @classmethod
    def register_multiple(cls):
        match request.method:
            case "GET": return cls.register_get()
            case "POST": return cls.register_post()

    
    @classmethod
    @auth_manager(anonimous=True)
    def login_get(cls):
        next = request.args.get("next")
        return render_template("auth/login.html", next=next)
    

    @classmethod
    @auth_manager(anonimous=True)
    def login_post(cls):
        if request.authorization is None: abort(400)
        auth = {
            "user": request.authorization.get("username"),
            "password": request.authorization.get("password")
        }
        if not all([auth["user"], auth["password"]]): abort(400)

        data = request.get_json()

        n = data.get("next")
        if n: n = str(base64.b64decode(n))[2:-1]

        user:User = User.query.filter_by(email=auth["user"]).first()
        if not user: user = User.query.filter_by(username=auth["user"]).first()
        if user:
            if user.check_password(password=auth["password"]):

                session["userID"] = user.id
                if data.get("keep"): session.permanent = True

                return jsonify(
                    { "location": n or url_for("webui.index", _external=True)}
                ), 200, {"Authorization": f"{create_access_jwt(user, keep=data.get('keep'))}"}
                
        abort(500)
    
    @classmethod
    @auth_manager(anonimous=True)
    def login_delete(cls):
        session.pop("user", None)
        return jsonify({ "location": url_for("auth.login") })


    @classmethod
    @auth_manager(anonimous=True)
    def register_get(cls):
        next = request.args.get("next")
        return render_template("auth/register.html", next=next)
    
    @classmethod
    @auth_manager(anonimous=True)
    def register_post(cls):

        attrs = [ "email", "birth", "name" ]
        data, d = request.get_json(), {}
        auth = {
            "username": request.authorization.get("username"),
            "password": request.authorization.get("password"),
        }

        n = data.get("next")
        if n: n = str(base64.b64decode(n))[2:-1]

        for k in attrs:
            if k not in data: abort(400)
            d[k] = data[k]
        
        if not User.query.filter_by(email=data["email"]).first():
            date = (int(i) for i in  d["birth"].split("-"))
            d["birth"] = datetime.datetime(*date)
            user = User(**d, **auth)
            g.db.session.add(user)
            g.db.session.commit()

            session["userID"] = user.id
            if data.get("keep"):session.permanent = True
            

            return jsonify(
                { "location": n or url_for("webui.index")}
            ),201, {
                "Authorization": f"Bearer {create_access_jwt(user, keep=data.get('keep'))}"
            }
        abort(400)

