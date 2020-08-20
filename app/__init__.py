from flask import Flask


def create_app(**kwargs):

    app = Flask(__name__, **kwargs)

    from image import image_api
    app.register_blueprint(image_api, url_prefix="/api/v1/image")

    return app
