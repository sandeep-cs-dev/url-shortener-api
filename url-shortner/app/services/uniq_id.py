import requests
from app.dto.uniq_id_dto import UniqIdDTO


def generate_uniq_id():
    url = "http://localhost:3000/generate-uniq-id"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        uniq_id_data = response.json()
        print(f"uniq_id_data {uniq_id_data}")
        return UniqIdDTO(uniq_id=uniq_id_data['id'])
    else:
        raise ValueError(f"Error: {response.status_code}")
