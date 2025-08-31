from flask import Flask
from flask_cors import CORS
from models import db, migrate
from api import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
