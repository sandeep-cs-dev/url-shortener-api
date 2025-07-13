from marshmallow import Schema, fields


class CreateShortUrlSchema(Schema):
    long_url = fields.Url(required=True)
