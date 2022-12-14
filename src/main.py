from flask import Flask
from init import db, ma, bcrypt, jwt 
from controllers.comic_controller import comics_bp
from controllers.auth_controller import auth_bp
from controllers.cli_controller import db_commands
from controllers.review_controller import review_bp
from marshmallow.exceptions import ValidationError
import os

def create_app():
    app = Flask(__name__)
    
    
    app.config ['JSON_SORT_KEYS'] = False
    # configuring database link 
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    # secret keys for tokens
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    
    # inititialization
    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    
    # registers blueprints from controllers
    app.register_blueprint(db_commands)
    app.register_blueprint(comics_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(review_bp)

    # catching errors
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400

    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400
    
    
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': 'You are not authorized to perform this action'}, 401

    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error': f'The field {err} is required.'}, 400


  


    return app
