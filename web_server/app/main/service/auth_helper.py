import flask_login

from app.main import login_manager
from app.main.model.user import User, SecurityUser
from app.main.service.blacklist_service import save_token


class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the security_user data
            security_user = SecurityUser.query.filter_by(username=data.get('username')).first()
            if security_user and security_user.check_password(data.get('password')):
                if flask_login.login_user(security_user.user):
                    return {'message': 'success login'}, 200
                else:
                    return {'message': 'user inactive'}, 401
            else:
                return {'message': 'invalid username or password'}, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if data:
            success, resp = User.decode_auth_token(auth_token)
            if success:
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_header = new_request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            success, resp = User.decode_auth_token(auth_token)
            if success:
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
