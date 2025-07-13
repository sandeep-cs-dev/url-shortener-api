from flask import Flask
from app.routes.short_url_route import create_short_url_bp

f_app = Flask(__name__)
f_app.register_blueprint(create_short_url_bp)
PORT = 4000


def start_server():
    f_app.run(port=PORT)
