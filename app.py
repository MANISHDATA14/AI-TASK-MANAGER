from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import os
from sqlalchemy.exc import DatabaseError, IntegrityError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from src.SharedServices.MainService import CustomError, errorResponse
from src.config.extension import db, ma, mail, socketio
from src.apps.api import apiBluePrint


def createApp():
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    app = Flask(__name__)

    # Cors Origin initialize
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize Flask-SocketIO
    socketio.init_app(app, cors_allowed_origins="*")

    # Flask configuration initialize
    app.config.from_pyfile('config/configurations.py')
    # Database connection initialize
    db.init_app(app)

    # Marshmallow initialize
    ma.init_app(app)

    # Flask mail initialize
    mail.init_app(app)

    # Register blueprints
    app.register_blueprint(apiBluePrint)

    @app.errorhandler(NotFound)
    def handle_not_found(error):
        return errorResponse(404, "Resource not found")

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        return errorResponse(400, str(error))

    @app.errorhandler(InternalServerError)
    def handle_internal_server_error(error):
        # Ideally, log the error details here for debugging
        return errorResponse(500, "An internal server error occurred")

    @app.errorhandler(CustomError)
    def handle_custom_error(error):
        return errorResponse(400, str(error))

    @app.errorhandler(DatabaseError)
    def handle_database_error(error):
        return errorResponse(500, "Database error occurred")

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        return errorResponse(400, "Integrity constraint violated")

    @app.errorhandler(500)
    def handle_500(error):
        app.logger.error(f"500 error occurred: {error}")
        return errorResponse(500, "Internal server error")

    return app
