from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def role_check(valid_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if 'roles' in claims:
                roles = claims['roles']

                for valid_role in valid_roles:
                    if valid_role in roles:
                        return fn(*args, **kwargs)

            return jsonify(msg='Missing Authorization Header'), 401

        return decorator

    return wrapper
