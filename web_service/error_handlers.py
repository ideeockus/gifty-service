from flask import Blueprint, jsonify
from pydantic import ValidationError
from models.api import CommonResponse, ResponseStatus

error_handler = Blueprint("error_handler", __name__)


class RequestFailed(Exception):
    def __repr__(self):
        return "Request Failed"


@error_handler.app_errorhandler(404)
def page_not_found(error):
    return "Error 404 Not Found"


@error_handler.app_errorhandler(RequestFailed)
def request_failed(error):
    print("Error handling")
    return jsonify(CommonResponse(
        status=ResponseStatus.Failed
    ))


@error_handler.app_errorhandler(ValidationError)
def validation_error(error: ValidationError):
    return jsonify(
        error.errors()
    )
