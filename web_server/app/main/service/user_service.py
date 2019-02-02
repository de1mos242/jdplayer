from app.main import db, login_manager
from app.main.model.user import User, SecurityUser


def create_admin():
    existed_admin = User.query.filter(User.username.is_('admin')).first()
    if existed_admin is None:
        admin = User(username='admin', admin=True)
        security_admin = SecurityUser(username='admin')
        security_admin.password = '123'
        security_admin.user = admin

        db.session.add(admin)
        db.session.add(security_admin)
        db.session.commit()
        db.session.flush()


def get_all_users():
    return User.query.all()


@login_manager.user_loader
def get_user_by_id(id):
    return User.load_by_id(id)


def save_changes(data):
    db.session.add(data)
    db.session.commit()
