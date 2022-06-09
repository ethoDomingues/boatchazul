[
    {   
        "default": {
            "app_cfg": {
                "template_folder": "front/html",
                "static_folder": "front/assets",
                "static_url_path": "/assets"
            },
            "cfg": {
                "SQLALCHEMY_TRACK_MODIFICATIONS": false,
                "SECRET_KEY": ".::[ TOP SECRET ]::.",
                "SERVER_NAME": "social.localhost:8080",
                "SESSION_COOKIE_HTTPONLY": false
            }
        },
        "testing": {
            "app_cfg": {},
            "cfg": {
                "TESTING": true,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"
            }
        },
        "production": {
            "app_cfg": {},
            "cfg": {
                "TESTING": true,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///prod.db"
            }
        },
        "development": {
            "app_cfg": {},
            "cfg": {
                "DEBUG": 1,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///dev.db"
            }
        }
    }
]