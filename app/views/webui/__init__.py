from flask import g
from flask import render_template

from app.views.auth.utils import auth_manager, create_access_jwt

@auth_manager(required=True)
def index(): return render_template("/webui/posts/post.html", JWT=create_access_jwt(g.user))

@auth_manager(required=True)
def groups(): return render_template("/webui/groups/groups.html", JWT=create_access_jwt(g.user))

@auth_manager(required=True)
def group(group):
    return render_template(
        "/webui/groups/group.html",
        group=g.db.tables.getObjectById(group, code_error=404),
        JWT=create_access_jwt(g.user)
    )

WEBUI_BP = {
    "cfg": {
        "name": "webui",
        "url_prefix": "/",
    },
    "routes": [
        {
            "rule": "",
            "methods": ["GET"],
            "endpoint": "index",
            "view_func": index,
        },
        {
            "rule": "/groups",
            "methods": ["GET"],
            "endpoint": "groups",
            "view_func": groups,
        },
        {
            "rule": "/groups/<string:group>",
            "methods": ["GET"],
            "endpoint": "group",
            "view_func": group,
        }
    ]
}