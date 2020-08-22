from flask import Flask
from flask_cors import CORS

from app.utils import get_config


def create_app(config_name=None, **kwargs):

    app = Flask(__name__, **kwargs)
    CORS(app)

    from app.database import init_db

    try:
        app.config.from_object(get_config(config_name))
    except ImportError:
        raise Exception('Invalid Config')

    from image import image_api
    app.register_blueprint(image_api, url_prefix="/api/v1/image")

    init_db(app)
    return app
