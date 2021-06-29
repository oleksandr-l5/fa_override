import os

import flask_admin
from flask import Flask, Blueprint, current_app, send_from_directory
from flask_admin import Admin, AdminIndexView
from flask_mongoengine import MongoEngine
from werkzeug.exceptions import NotFound

from views import ExampleView


class Config:
    SECRET_KEY = 'oWEhH7WaFAbtquLQ'
    MONGODB_SETTINGS = {'db': 'fa_override', 'host': 'mongodb+srv://cluster0.tp437.mongodb.net/myFirstDatabase',
                        'alias': 'default', 'username': 'fa_override', 'password': 'oWEhH7WaFAbtquLQ'}


def _send_static_file(filename):
    max_age = 31536000
    try:
        return send_from_directory(os.path.join(current_app.root_path, "static/fa_override"), filename, max_age=max_age)
    except NotFound:
        return send_from_directory(os.path.join(flask_admin.__path__[0], "static"), filename, max_age=max_age)


class IndexView(AdminIndexView):
    def create_blueprint(self, admin):
        self.admin = admin
        self.url = self._get_view_url(admin, self.url)
        if self.url == '/':
            self.url = None
        if self.name is None:
            self.name = self._prettify_class_name(self.__class__.__name__)
        self.blueprint = Blueprint(self.endpoint, __name__, url_prefix=self.url, subdomain=self.admin.subdomain,
                                   template_folder=os.path.join('templates', self.admin.template_mode),
                                   root_path=flask_admin.__path__[0])
        for url, name, methods in self._urls:
            self.blueprint.add_url_rule(url, name, getattr(self, name), methods=methods)
        return self.blueprint


flask_app = Flask(__name__, root_path=os.getcwd(), template_folder='templates', static_folder=None)
flask_app.config.from_object(Config)
flask_app.add_url_rule("/static/<path:filename>", view_func=_send_static_file, endpoint="static")
flask_app.add_url_rule("/static/<path:filename>", view_func=_send_static_file, endpoint="admin.static")
admin_app = Admin(flask_app, name="", url="/", template_mode="bootstrap4",
                  index_view=IndexView(url='/', name="Home"))
MongoEngine().init_app(flask_app)
admin_app.add_view(ExampleView(name="Example"))

if __name__ == "__main__":
    flask_app.run('localhost', 9090)
