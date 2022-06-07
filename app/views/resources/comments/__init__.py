
from .functions import COMMFunctions


COMMENTS_ROUTES = [
    {
        "rule":"/comments",
        "methods":["POST"],
        "endpoint":"comments_post",
        "view_func": COMMFunctions.post,
    },
    {
        "rule":"/comments/<string:comm>",
        "methods":["GET", "PUT", "DELETE"],
        "endpoint":"comments",
        "view_func": COMMFunctions.multiple,
    }
]