from flask import Blueprint
from flask_restplus import Api

from app.main.controller.namespaces import user_ns, auth_ns, track_ns, room_ns
from app.main.model import track, user, room, playlist

blueprint = Blueprint('api', __name__, url_prefix='/api')

authorizations = {
    'Cookies Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Cookies'
    },
}

api = Api(blueprint,
          title='JD Player API',
          version='1.0',
          description='collective streaming audio player',
          security='Cookies Auth',
          authorizations=authorizations
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(track_ns, path='/track')
api.add_namespace(room_ns, path='/room')
