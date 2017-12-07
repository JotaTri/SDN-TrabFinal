import jose.jwt as jwt

import traceback


secret_key_imob = 'SenhaSuperMegaDificil'

options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}

def authenticated(handler_class):
    def wrap_execute(handler_execute):
        def require_auth(handler, kwargs):
            auth = handler.request.headers.get('Authorization')
            if auth:
                parts = auth.split()

                if parts[0].lower() != 'bearer':
                    response = {
                        'status': 'error',
                        'info': 'invalid header authorization'
                    }
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write(response)
                    handler.finish()
                elif len(parts) == 1:
                    response = {
                        'status': 'error',
                        'info': 'invalid header authorization'
                    }
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write(response)
                    handler.finish()
                elif len(parts) > 2:
                    response = {
                        'status': 'error',
                        'info': 'invalid header authorization'
                    }
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write(response)
                    handler.finish()

                token = parts[1]
                try:
                    info = jwt.decode(
                        token,
                        secret_key_imob,
                    )
                except jwt.ExpiredSignatureError:
                    response = {
                        'status': 'error',
                        'info': 'expired token'
                    }
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write(response)
                    handler.finish()
                except:
                    response = {
                        'status': 'error',
                        'info': 'unknown error'
                    }
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write(response)
                    handler.finish()
            else:
                response = {
                    'status': 'error',
                    'info': 'missing headers'
                }
                handler._transforms = []
                handler.set_status(400)
                handler.write(response)
                handler.finish()
            handler.request.headers.add('auth', info)
            return True

        def _execute(self, transforms, *args, **kwargs):

            try:
                require_auth(self, kwargs)
            except:
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class
