from flask import Blueprint, jsonify, request, g
from app.dto.create_short_url_schema import CreateShortUrlSchema
from marshmallow import ValidationError

from app.services.short_url import generate_short_url

create_short_url_bp = Blueprint('create_short_url', __name__)

create_short_url_schema = CreateShortUrlSchema()


@create_short_url_bp.before_request
def validate_request():
    try:
        long_url_data = create_short_url_schema.load(request.json)
        g.data = long_url_data
    except ValidationError as err:
        return jsonify(err.messages), 400


@create_short_url_bp.route('/generate-short-url', methods=["POST"])
def create_short_url():
    data = g.data
    short_id = generate_short_url()
    return jsonify({"msg": "success", 'short_id': short_id}), 201
