from .functions import POSTSFunctions

POSTS_ROUTES = [
    {
        "rule":"/posts",
        "methods": ["POST"],
        "endpoint":"post_post",
        "view_func": POSTSFunctions.post,
    },
    {
        "rule":"/posts/list",
        "methods": ["GET"],
        "endpoint":"post_get_list",
        "view_func": POSTSFunctions.get_list,
    },
    {
        "rule":"/posts/all",
        "methods": ["GET"],
        "endpoint":"post_get_all",
        "view_func": POSTSFunctions.get_all,
    },
    {
        "rule":"/posts/<string:post>",
        "methods": ["GET", "PUT", "DELETE"],
        "endpoint":"post",
        "view_func": POSTSFunctions.multiple,
    }
]