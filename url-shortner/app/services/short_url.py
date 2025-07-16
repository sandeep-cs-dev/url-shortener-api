from app.dto.uniq_id_dto import UniqIdDTO
from app.services.uniq_id import generate_uniq_id
from app.util.num_to_short_id import base62_encode


def generate_short_url():
    uniq_id: UniqIdDTO = generate_uniq_id()
    uid = uniq_id.uniq_id % (67 ** 7)
    short_id = base62_encode(uid)
    return short_id
