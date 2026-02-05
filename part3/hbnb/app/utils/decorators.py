from functools import wraps
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt,
    get_jwt_identity
)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {"error": "Admin privileges required"}, 403

        return fn(*args, **kwargs)
    return wrapper

def owner_or_admin_required(get_resource):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            claims = get_jwt()
            user_id = get_jwt_identity()
            is_admin = claims.get("is_admin", False)

            resource = get_resource(*args, **kwargs)
            if not resource:
                return {"error": "Resource not found"}, 404

            owner_id = getattr(resource, "owner_id", None) or getattr(resource, "user_id", None) or getattr(resource, "id", None)

            if not is_admin and owner_id != user_id:
                return {"error": "Unauthorized action"}, 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
