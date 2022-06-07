from .functions import CDNFunctions


CDN_BP = {
    "cfg": {
        "name": "cdn",
        "subdomain": "cdn",
    },
    "routes": [
        {
            "rule": "/all",
            "methods": ["GET"],
            "endpoint": "get_all",
            "view_func": CDNFunctions.get_all,
        },
        {
            "rule": "/",
            "methods": ["POST"],
            "endpoint": "post",
            "view_func": CDNFunctions.post,
        },
        {
            "rule": "/<string:cdn>/<string:filename>",
            "methods": ["GET"],
            "endpoint": "get",
            "view_func": CDNFunctions.get,
        }
    ]
}