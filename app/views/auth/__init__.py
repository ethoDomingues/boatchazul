from .functions import AUTHFunctions



AUTH_BP = {
    "cfg": {
        "name": "auth",
        "subdomain": "auth",
    },
    "routes": [
        {
            "rule": "/login",
            "methods": ["GET", "POST", "DELETE"],
            "endpoint": "login",
            "view_func": AUTHFunctions.login_multiple,
        },
        {
            "rule": "/register",
            "methods": ["GET", "POST"],
            "endpoint": "register",
            "view_func": AUTHFunctions.register_multiple,
        }
    ]
}