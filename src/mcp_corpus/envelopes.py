"""Small structured result envelope helpers."""


def ok(message, data):
    return {
        "status": "ok",
        "message": message,
        "data": data,
    }


def error(error_code, message, data=None):
    if data is None:
        data = {}

    return {
        "status": "error",
        "error_code": error_code,
        "message": message,
        "data": data,
    }
