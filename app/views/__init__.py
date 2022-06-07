
from flask import Flask
from flask import Blueprint
from flask import Response

from flask import g
from flask import session
from flask import request

from app.model import db

from app.views.auth.utils import create_access_jwt
from app.views.auth.utils import validate_access_jwt

from .cdn import CDN_BP
from .auth import AUTH_BP
from .webui import WEBUI_BP
from .resources import API_BP


bps = [ CDN_BP, AUTH_BP, WEBUI_BP, API_BP ]

rules = {}

class Views:

    def __init__(self, app:"Flask") -> None:
        for bp_raw in bps:
            bp = Blueprint(
                import_name = "app",
                
                name = bp_raw["cfg"].get("name"),
                root_path = bp_raw["cfg"].get("root_path"),
                subdomain = bp_raw["cfg"].get("subdomain"),
                url_prefix = bp_raw["cfg"].get("url_prefix"),
                url_defaults = bp_raw["cfg"].get("url_defaults"),
                static_folder = bp_raw["cfg"].get("static_folder"),
                static_url_path = bp_raw["cfg"].get("static_url_path"),
                template_folder = bp_raw["cfg"].get("template_folder"),
            )

            for route in bp_raw["routes"]:
                bp.add_url_rule(
                    rule = route["rule"],
                    methods = route["methods"],
                    endpoint = route["endpoint"],
                    view_func = route["view_func"],
                )
                rules[f'{bp.name}.{route["endpoint"]}'] = route["methods"]
            app.register_blueprint(bp)
            del bp
        app.before_request(before_request)
        app.after_request(after_request)
        
    
def before_request():

    if "db" not in g: g.db = db
    if "rules" not in g: g.rules = rules
    if "user" not in g:
        g.user = None
        jwt = request.headers.get("Authorization")
        if session.get("userID"):
            g.user = db.tables.getObjectById(session.get("userID"))
            if g.user is None: session.pop("userID")
        if jwt is not None and request.blueprint != 'auth':
            jwt = jwt.split(" ")
            if len(jwt) == 2 and jwt[0] == "Bearer":
                payload = validate_access_jwt(jwt[1])
                if payload: g.user = db.tables.getObjectById(payload.get("userID"))
        if g.user is None: g.pop("user", None)
        



def after_request( response:Response ):
    if not request.endpoint in g.rules: return response

    if request.endpoint not in [ "webui" ]:
        methods = g.rules[request.endpoint]
        response.headers.add("Access-Control-Allow-Origin", '*')
        response.headers.add("Access-Control-Allow-Methods", ",".join(methods))
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Max-Age","86400")

        
    return response