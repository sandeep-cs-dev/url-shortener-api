from app.routes.uniq_id import uniq_id_route
from flask import Flask

f_app = Flask(__name__)
f_app.register_blueprint(uniq_id_route)
if __name__ == "__main__":
    f_app.run(port=3000)
