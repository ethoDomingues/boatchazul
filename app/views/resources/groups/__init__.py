
from .functions import GROUPFunctions
from .functions.grouphook import GROUPHOOKFunction


GROUP_ROUTES = [
    {
        "rule": "/groups",
        "methods": ["POST"],
        "endpoint": "group_post",
        "view_func": GROUPFunctions.post,
    },
    {
        "rule": "/groups",
        "methods": ["GET"],
        "endpoint": "group_get_all",
        "view_func": GROUPFunctions.get_all,
    },
    {
        "rule": "/groups/<string:group>",
        "methods": ["GET", "PUT", "DELETE"],
        "endpoint": "group",
        "view_func": GROUPFunctions.multiple,
    }

]

GROUPHOOK_ROUTES = [
    {
        "rule": "/grouphook/<string:group>",
        "methods": ["POST", "PUT", "DELETE"],
        "endpoint": "grouphook",
        "view_func": GROUPHOOKFunction.multiple,
    }
]