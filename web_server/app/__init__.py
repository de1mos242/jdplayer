from flask import Blueprint
from flask_restplus import Api

from app.main.controller.user_controller import api as user_ns
from app.main.controller.auth_controller import api as auth_ns

blueprint = Blueprint('api', __name__)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api = Api(blueprint,
          title='JD Player API',
          version='1.0',
          description='collective streaming audio player',
          security='Bearer Auth',
          authorizations=authorizations
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)