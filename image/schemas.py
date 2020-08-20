from marshmallow import Schema, fields, post_load, validates, ValidationError


class ImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    file_name = fields.Str(required=True)
    description = fields.Str(required=True)
    thumbnail_name = fields.Str(dump_only=True)
    format = fields.Str(dump_only=True)
    dimensions = fields.Str(dump_only=True)
