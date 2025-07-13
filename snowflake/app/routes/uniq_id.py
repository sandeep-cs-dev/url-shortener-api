from app.services.unique_id import generate_uniq_id
from flask import Blueprint

uniq_id_route = Blueprint('uniq_id', __name__)


@uniq_id_route.route('/generate-uniq-id')
def get_uniq_id():
    uniq_id = generate_uniq_id()
    return dict(id=uniq_id)
