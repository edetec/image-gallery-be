import uuid
from pathlib import Path

from flask import current_app


def handle_image_upload(model, image):
    image_path = current_app.config['IMAGES_PATH']
    image_format = image.format
    file_name = f"{uuid.uuid4()}.{image_format.lower()}"

    model.file_path = f"{image_path}/{file_name}"
    model.thumbnail_path = f"{image_path}/thumbnail-{file_name}"
    model.dimensions = f"{image.height}x{image.width}"
    model.format = image_format


def save_image_files(model, image):
    root_app = Path(current_app.config['ROOT_DIR'])
    image.save(root_app.joinpath(model.file_path))
    image.thumbnail((100, 100))
    image.save(root_app.joinpath(model.thumbnail_path))


def remove_image_file(file):
    if file is None:
        return
    root_app = Path(current_app.config['ROOT_DIR'])
    file_path = root_app.joinpath(file)
    if file_path.is_file():
        file_path.unlink(missing_ok=True)
