from flask import Flask, render_template
from flask.json import JSONEncoder
from admin_panel import admin_panel
from common_api import user_api
from error_handlers import error_handler
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

import secrets
import logging


class ServiceCustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, BaseModel):
                return obj.dict()

            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.secret_key = secrets.token_bytes(30)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1000 * 1000  # in bytes
app.register_blueprint(admin_panel)
app.register_blueprint(user_api)
app.register_blueprint(error_handler)
app.logger.setLevel(logging.DEBUG)
app.json_encoder = ServiceCustomJsonEncoder

print(app.url_map)


@app.route('/')
def index():
    return render_template("user/index.html")


if __name__ == '__main__':
    app.run(debug=True)
