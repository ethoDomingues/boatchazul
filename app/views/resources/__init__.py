
from .posts import POSTS_ROUTES
from .reacts import REACTS_ROUTES
from .groups import GROUP_ROUTES
from .groups import GROUPHOOK_ROUTES
from .comments import COMMENTS_ROUTES
from .friends import FRIENDS_ROUTES
from .users import USER_ROUTES


API_BP = {
    "cfg": {
        "name": "api",
        "url_prefix": "/v1",
        "subdomain": "api"
    },
    "routes": [
        * POSTS_ROUTES,
        * REACTS_ROUTES,
        * COMMENTS_ROUTES,
        * FRIENDS_ROUTES,
        * GROUP_ROUTES,
        * GROUPHOOK_ROUTES,
        * USER_ROUTES
    ]
}