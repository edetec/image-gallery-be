from http import HTTPStatus

from flask import Blueprint, jsonify, request

from image.models import Image
from image.schemas import ImageSchema

image_api = Blueprint('image_api', __name__)


def apply_filters(query):
    args = request.args
    if 'description' in args:
        filter_param = args['description']
        query = query.filter(Image.description.ilike(f"%{filter_param}%"))
    if 'dimensions' in args:
        filter_param = args['dimensions']
        query = query.filter(Image.dimensions == filter_param)
    if 'format' in args:
        filter_param = args['format']
        query = query.filter(Image.format == filter_param)
    return query


@image_api.route("/", methods=['GET'])
def get_all():
    query = apply_filters(Image.query)
    images = query.all()
    dumped = ImageSchema(many=True).dump(images)
    return jsonify(dumped), HTTPStatus.OK
