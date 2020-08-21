from marshmallow import Schema, fields, post_load, validates, ValidationError


class ImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    file_path = fields.Str(required=True)
    thumbnail_path = fields.Str(dump_only=True)
    description = fields.Str(required=True)
    format = fields.Str(dump_only=True)
    dimensions = fields.Str(dump_only=True)
