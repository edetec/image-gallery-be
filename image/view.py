import functools
import operator
from http import HTTPStatus

from PIL import Image
from flask import Blueprint, jsonify, request
from sqlalchemy import distinct

from app.database import db
from image.models import ImageModel
from image.schemas import ImageSchema
from image.utils import handle_image_upload, save_image_files, remove_image_file, is_allowed_file, get_allowed_image_ext

image_api = Blueprint('image_api', __name__)


def apply_filters(query):
    args = request.args
    if 'description' in args:
        filter_param = args['description']
        query = query.filter(ImageModel.description.ilike(f"%{filter_param}%"))
    if 'dimensions' in args:
        filter_param = args['dimensions']
        query = query.filter(ImageModel.dimensions == filter_param)
    if 'format' in args:
        filter_param = args['format'].lower()
        query = query.filter(ImageModel.format == filter_param)
    return query


@image_api.route("/", methods=['GET'])
def get_all():
    query = apply_filters(ImageModel.query)
    images = query.all()
    dumped = ImageSchema(many=True).dump(images)
    return jsonify(dumped), HTTPStatus.OK


@image_api.route("/dimensions/", methods=['GET'])
def get_all_dimensions():
    dimensions = db.session.query(distinct(ImageModel.dimensions)).all()
    flat_list = functools.reduce(operator.iconcat, dimensions) if dimensions else []
    return jsonify(flat_list), HTTPStatus.OK


@image_api.route("/", methods=['POST'])
def upload():
    file = request.files.get('file')
    description = request.form.get('description')
    if not file:
        return jsonify({'error': 'File is required'}), HTTPStatus.BAD_REQUEST
    if not description:
        return jsonify({'error': 'Description is required'}), HTTPStatus.BAD_REQUEST

    image = Image.open(file)
    if not is_allowed_file(image):
        ext_list = get_allowed_image_ext()
        return jsonify({'error': f'This file is not one among allowed file types [{ext_list}]'}), HTTPStatus.BAD_REQUEST

    model = ImageModel(description=description)
    handle_image_upload(model, image)

    db.session.add(model)
    db.session.commit()
    save_image_files(model, image)

    dumped = ImageSchema().dump(model)
    return jsonify(dumped), HTTPStatus.CREATED


@image_api.route("/<int:image_id>", methods=['PUT'])
def upload_update(image_id):
    file = request.files.get('file')
    description = request.form.get('description')
    if not description:
        return jsonify({'error': 'Description is required'}), HTTPStatus.BAD_REQUEST

    model = ImageModel.query.get(image_id)
    if not model:
        return jsonify({'error': 'Not found'}), HTTPStatus.NOT_FOUND

    model.description = description

    if file is not None:
        old_file = model.file_path
        old_thumbnail = model.thumbnail_path
        image = Image.open(file)
        if not is_allowed_file(image):
            ext_list = get_allowed_image_ext()
            return (jsonify({'error': f'This file is not one among allowed file types [{ext_list}]'}),
                    HTTPStatus.BAD_REQUEST)
        handle_image_upload(model, image)

    db.session.add(model)
    db.session.commit()

    if file is not None:
        save_image_files(model, image)
        remove_image_file(old_file)
        remove_image_file(old_thumbnail)

    dumped = ImageSchema().dump(model)
    return jsonify(dumped), HTTPStatus.OK
