from app import create_app
import os
from flask_script import Manager

app = create_app(os.environ['CONFIG_TYPE'])
manager = Manager(app)


@manager.command
def run():
    """Like a 'runserver' command but shorter, lol."""
    app.run()


if __name__ == '__main__':
    manager.run()
