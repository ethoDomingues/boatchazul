from flask import g
from flask import jsonify


from app.views.auth.utils import auth_manager


@auth_manager(required=True)
def react(owner:str):
    p = g.db.tables.getObjectById(owner, code_error=404)
    p.reacts = g.user
    return jsonify(p.to_dict())



REACTS_ROUTES = [
    {
        "rule": "reacts/<string:owner>",
        "methods": ["POST"],
        "endpoint": "reacts_post",
        "view_func": react,
    }

]