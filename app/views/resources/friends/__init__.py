from .functions import FRIENDSFunction


FRIENDS_ROUTES = [
    {
        "rule":"/friends",
        "methods":["POST"],
        "endpoint":"friends_post",
        "view_func": FRIENDSFunction.post,
    },
    {
        "rule":"/friends/<string:user>",
        "methods":["GET","PUT", "DELETE"],
        "endpoint":"friends",
        "view_func": FRIENDSFunction.multiple,
    }
]