import unittest

from app.main import db
from app.main.model.user import User, SecurityUser, UserSource
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):
    def test_store_security_user(self):
        user = User(username='t1000', source=UserSource.security)
        security_user = SecurityUser(username='t1000', user=user)
        security_user.password = '1000'

        self.assertIsNotNone(security_user.password_hash)

        db.session.add(user)
        db.session.add(security_user)
        db.session.commit()
        db.session.flush()

        db_s_user = SecurityUser.query.filter(SecurityUser.username == 't1000').first()
        self.assertIsNotNone(db_s_user, 'security user not saved')
        self.assertEquals(db_s_user.user.username, 't1000')

if __name__ == '__main__':
    unittest.main()
