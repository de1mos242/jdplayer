import flask_login

from app.main.model.user import SecurityUser


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
    def logout_user():
        flask_login.logout_user()
