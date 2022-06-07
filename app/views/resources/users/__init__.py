from flask import g
from flask import jsonify

from app.views.auth.utils import auth_manager


@auth_manager()
def get_user(user): return jsonify(g.db.tables.getObjectById(user, code_error=404).to_dict(_complete=True))

@auth_manager(required=True)
def whoami(): return jsonify(g.user.to_dict(_complete=True))



USER_ROUTES = [
    {
        "rule": "/users/<string:user>",
        "methods": ["GET"],
        "endpoint": "users",
        "view_func": get_user,
    },
    {
        "rule": "/users/whoami",
        "methods": ["GET"],
        "endpoint": "whoami",
        "view_func": whoami,
    },
]