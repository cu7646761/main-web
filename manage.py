import unittest

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from flasky import app
from app import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """ Runs the unit tests. """
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
