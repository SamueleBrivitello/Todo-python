from flask import Flask
from flask_cors import CORS
from database import init_db
from routes import register_routes

app = Flask(__name__)
CORS(app)
init_db()
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
