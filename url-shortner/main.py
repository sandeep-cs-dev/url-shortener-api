from app import app

try:
    app.start_server()
except Exception as e:
    print(f" unhandled exception {e}")
