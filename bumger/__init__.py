import os

from flask import Flask

def create_app(test_config=None):
    app = Flask('bumger', instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from bumger.payments import receipt
    app.register_blueprint(receipt.bp)
    app.add_url_rule('/', endpoint='index')

    from bumger.payments import payment
    app.register_blueprint(payment.bp)

    from bumger.expenses import expense
    app.register_blueprint(expense.bp)

    return app
