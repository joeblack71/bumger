import os

from flask import Flask
#from flask_mail import Mail

def create_app(test_config=None):
    app = Flask('manager', instance_relative_config=True)
    #mail = Mail(app)

    ##app.config.from_mapping(
    ##    SECRET_KEY='dev',
    ##    DATABASE=os.path.join(app.instance_path,'dev_manager.sqlite'),
    ##)

    ##app.config.from_pyfile('settings.cfg') # default settings
    ##app.config.from_envvar('BUMGER_SETTINGS')

    app.config['SECRET_KEY'] = os.environ.get("BUMGER_SECRET_KEY")
    app.config['DATABASE'] = os.path.join(app.instance_path, os.environ.get("BUMGER_DATABASE"))

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #from . import user
    #app.register_blueprint(user.bp)

    from . import db
    db.init_app(app)

    ##from . import index
    ##app.register_blueprint(index.bp)

    from . import receipt
    app.register_blueprint(receipt.bp)

    from . import payment
    app.register_blueprint(payment.bp)

    ##from . import expense
    ##app.register_blueprint(expense.bp)

    return app
