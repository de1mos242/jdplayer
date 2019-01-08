from flask import request
from flask_restplus import Resource
from vk_api import vk_api
from vk_api.audio import VkAudio

from app.main.controller.namespaces import auth_ns as api
from app.main.service.auth_helper import Auth
from app.main.util.decorator import token_required
from app.main.util.dto import AuthDto

user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """

    @api.doc('user login', security=None)
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """

    @token_required
    @api.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)


@api.route('/facebook')
class LoginFacebook(Resource):
    """
    Login though facebook
    """

    @api.doc('facebook login')
    def post(self):
        print(request)
        return {"status": request, 'access_token': 'fdsafsad'}, 200


@api.route('/vk')
class LoginFacebook(Resource):
    """
    Login though vk
    """

    @api.doc('vk login')
    def post(self):
        print(request)
        vk_session = vk_api.VkApi(app_id=3380204, client_secret='Ky3xN0ohvtMzaVgCYU80')
        vk_session.code_auth(request.json()['code'], request.json()['redirectUri'])
        token = vk_session.token['access_token']

        vkaudio = VkAudio(vk_session)
        print([x for x in vkaudio.search('sandstorm')])
        """
        'code' (139893782146720) = {str} 'f2addb2855bb6b95b5'
'clientId' (139893782181168) = {str} '3380204'
'redirectUri' (139893782180784) = {str} 'https://192.168.20.37:8080/'
        """
        return {"status": request, 'access_token': 'fdsafsad'}, 200
