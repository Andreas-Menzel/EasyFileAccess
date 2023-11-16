import functools


def error_to_http_response(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except FileNotFoundError as e:
            return {'message': str(e)}, 404
        except FilePathInvalidError as e:
            return {'message': str(e)}, 400
        except FileAlreadyExistsError as e:
            return {'message': str(e)}, 409
        except FileNotProvidedError as e:
            return {'message': str(e)}, 400
        except BaseException as e:
            return {'message': str(e)}, 500

    return decorated_function


class FilePathInvalidError(Exception):
    pass


class FileAlreadyExistsError(Exception):
    pass


class FileNotProvidedError(Exception):
    pass
