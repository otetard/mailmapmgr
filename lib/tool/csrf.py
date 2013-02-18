# -*- coding: utf-8 -*-

import cherrypy
from Crypto import Random
from base64 import b64encode, b64decode

CSRF_KEY_LENGTH = 32
CSRF_SESSION_KEY = "_cp_csrftoken"
CSRF_COOKIE = "csrftoken"

class CsrfTool(cherrypy.Tool):

    def __init__(self):
        #super(CsrfTool, self).__init__('before_handler', self.log_start)

        self._point = "before_handler"
        self._name = None
        self._priority = 1
        # set the args of self.callable as attributes on self
        self._setargs()
        # a log for storing our per-path traffic data
        self._log = {}
        # a history of the last alert for a given path
        self._history = {}
        self.__doc__ = self.callable.__doc__
        self._struct = []

    def _generate_token(self):
        r = Random.new()
        return b64encode(r.read(CSRF_KEY_LENGTH))

    def _verify_token(self, token1, token2):
        if len(token1) != len(token2):
            return False

        return token1 == token2

    def set_csrf_cookie(self):
        cookie = cherrypy.response.cookie

        cookie[CSRF_COOKIE] = self.token_value
        cookie[CSRF_COOKIE]['path'] = '/'
        cookie[CSRF_COOKIE]['max-age'] = 3600  # FIXME! Corriger date expiration
        cookie[CSRF_COOKIE]['version'] = 1

        body = cherrypy.response.body

        if isinstance(body, dict):
            body.update({'csrftoken': self.token_value})

    def callable(self, enable=True):
        try:
            csrf_token = cherrypy.request.cookie[CSRF_COOKIE].value
            self.token_value = csrf_token
        except KeyError:
            csrf_token = None
            self.token_value = self._generate_token()

        cherrypy.request.csrftoken = self.token_value

        if enable:
            if cherrypy.request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
                if csrf_token is None:
                    raise cherrypy.HTTPError("403 Forbidden", "No CSRF Cookie")

                try:
                    request_csrf_token = cherrypy.request.params.pop('csrftoken')
                except KeyError:
                    request_csrf_token = ""

                    if not self._verify_token(request_csrf_token, csrf_token):
                        cherrypy.log("Invalid CSRF Token ({0} vs {1})")
                        raise cherrypy.HTTPError("403 Forbidden", "Invalid CSRF Token".format(request_csrf_token, csrf_token))
                    
            cherrypy.request.hooks.attach('before_finalize', self.set_csrf_cookie, priority=20)

