from http import HTTPStatus

from flask import Blueprint, jsonify

image_api = Blueprint('image_api', __name__)


@image_api.route("/", methods=['GET'])
def get_all():
    return jsonify([]), HTTPStatus.OK
