import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import db, app
# noinspection PyUnresolvedReferences
from app.main.controller import auth_controller, user_controller, track_controller, room_controller
from app.main.service import user_service

app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


def pre_run():
    with app.app_context():
        db.init_app(app)
        user_service.create_admin()


@manager.command
def run():
    pre_run()
    """Run application."""
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(descriptions=True, verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
