from app.config import Config
from app.model import Model
from app.views import Views

def create_app():
    app = Config("development")

    Model(app)
    Views(app)

    return app